"""Executa o processamento da capa dos processos PJE.

Este módulo contém a classe Capa responsável por autenticar, enfileirar e
processar processos judiciais, além de realizar o download da cópia integral
dos processos e salvar os resultados no storage.

"""

from __future__ import annotations

import secrets
import traceback
from concurrent.futures import (
    Future,
    ThreadPoolExecutor,
    as_completed,
)
from contextlib import suppress
from pathlib import Path
from threading import Semaphore, Thread
from time import sleep
from typing import TYPE_CHECKING, ClassVar

from dotenv import load_dotenv
from httpx import Client, Response
from tqdm import tqdm

from crawjud.common.exceptions.bot import (
    ExecutionError,
    FileUploadError,
)
from crawjud.controllers.pje import PjeBot
from crawjud.custom.task import ContextTask
from crawjud.decorators import shared_task, wrap_cls
from crawjud.interfaces.pje import (
    AssuntosProcessoPJeDict,
    AudienciaProcessoPjeDict,
    CapaProcessualPJeDict,
    PartesProcessoPJeDict,
    RepresentantePartesPJeDict,
)
from crawjud.interfaces.types import BotData
from crawjud.interfaces.types.bots.pje import (
    DictResults,
)
from crawjud.resources.elements import pje as el
from crawjud.utils.formatadores import formata_tempo

if TYPE_CHECKING:
    from httpx import Response

    from crawjud.interfaces.pje import ProcessoJudicialDict
    from crawjud.interfaces.pje.assuntos import AssuntoDict, ItemAssuntoDict
    from crawjud.interfaces.pje.audiencias import AudienciaDict
    from crawjud.interfaces.pje.partes import ParteDict, PartesJsonDict
    from crawjud.interfaces.types import BotData, DictType
    from crawjud.interfaces.types.bots.pje import DictResults
load_dotenv()

SENTINELA = None
workdir = Path(__file__).cwd()
semaforo_arquivo: Semaphore = Semaphore(10)
semaforo_processo: Semaphore = Semaphore(10)


@shared_task(name="pje.capa", bind=True, base=ContextTask)
@wrap_cls
class Capa(PjeBot):
    """Gerencia autenticação, enfileiramento e processamento de processos PJE.

    Esta classe executa autenticação, enfileiramento, processamento e download
    da cópia integral dos processos judiciais no sistema PJE, salvando os
    resultados no armazenamento definido.

    """

    to_add_partes: ClassVar[list[PartesProcessoPJeDict]] = []
    to_add_processos: ClassVar[list[CapaProcessualPJeDict]] = []
    to_add_assuntos: ClassVar[list[AssuntosProcessoPJeDict]] = []
    to_add_audiencias: ClassVar[list[AudienciaProcessoPjeDict]] = []
    to_add_representantes: ClassVar[list[RepresentantePartesPJeDict]] = []

    futures_download_file: ClassVar[list[Future]] = []

    def execution(self) -> None:
        """Executa o fluxo principal de processamento da capa dos processos PJE.

        Args:
            name (str | None): Nome do bot.
            system (str | None): Sistema do bot.
            current_task (ContextTask): Tarefa atual do Celery.
            storage_folder_name (str): Nome da pasta de armazenamento.
            *args (T): Argumentos variáveis.
            **kwargs (T): Argumentos nomeados variáveis.

        """
        generator_regioes = self.regioes()
        lista_nova = list(generator_regioes)

        self.pbar = tqdm(total=len(self._frame))

        with ThreadPoolExecutor(max_workers=24) as executor:
            futures: list[Future] = []
            for pos, t_regiao in enumerate(lista_nova):
                regiao, data_regiao = t_regiao

                if self.event_stop_bot.is_set():
                    break

                url = el.LINK_AUTENTICACAO_SSO.format(regiao=regiao)
                self.driver.get(url)
                headers, cookies = self.get_headers_cookies(regiao=regiao)

                futures.append(
                    executor.submit(
                        self.queue_regiao,
                        regiao=regiao,
                        data_regiao=data_regiao,
                        headers=headers,
                        cookies=cookies,
                        pos=pos,
                    ),
                )
                sleep(10)

            for future in futures:
                with suppress(Exception):
                    future.result()

        for to_save, sheet_name in [
            (self.to_add_processos, "Capa"),
            (self.to_add_audiencias, "Audiências"),
            (self.to_add_assuntos, "Assuntos"),
            (self.to_add_partes, "Partes"),
            (self.to_add_representantes, "Representantes"),
        ]:
            self.queue_save_xlsx.put({
                "to_save": to_save,
                "sheet_name": sheet_name,
            })

        self.thread_copia_integral.join()
        self.finalize_execution()

    def queue_regiao(
        self,
        regiao: str,
        data_regiao: list[BotData],
        headers: DictType,
        cookies: DictType,
        pos: int,
    ) -> None:
        pool_exe = ThreadPoolExecutor(max_workers=16)

        client_context = Client(cookies=cookies, headers=headers)

        self.thread_copia_integral = Thread(
            target=self.copia_integral,
            daemon=True,
            name=f"Salvar Cópia Integral Thread-{pos}",
        )

        self.thread_copia_integral.start()

        with client_context as client, pool_exe as executor:
            futures: list[Future] = []
            for item in data_regiao:
                if self.event_stop_bot.is_set():
                    break

                futures.append(
                    executor.submit(
                        self.queue,
                        item=item,
                        client=client,
                        regiao=regiao,
                    ),
                )
                sleep(2)
            for future in as_completed(futures):
                with suppress(Exception):
                    future.result()

    def queue(
        self,
        item: BotData,
        client: Client,
        regiao: str,
    ) -> None:
        try:
            if not self.event_stop_bot.is_set():
                processo = item["NUMERO_PROCESSO"]
                row = self.posicoes_processos[item["NUMERO_PROCESSO"]] + 1
                resultados: DictResults = self.search(
                    data=item,
                    row=row,
                    client=client,
                    regiao=regiao,
                )
                sleep(0.5)
                if not isinstance(resultados, dict):
                    self.print_msg(
                        message=str(resultados),
                        type_log="error",
                        row=row,
                    )

                    return

                self.capa_processual(
                    result=resultados["data_request"],
                    regiao=regiao,
                    row=row,
                )

                sleep(0.5)

                self.outras_informacoes(
                    numero_processo=processo,
                    client=client,
                    id_processo=resultados["id_processo"],
                    regiao=regiao,
                    row=row,
                )

                type_log = "success"
                message = "Execução Efetuada com sucesso!"

                if item.get("TRAZER_COPIA", "N").lower() == "s":
                    type_log = "info"

                    file_name = f"CÓPIA INTEGRAL - {processo} - {self.pid}.pdf"
                    self.queue_files.put({
                        "file_name": file_name,
                        "row": row,
                        "client": client,
                        "processo": processo,
                        "id_processo": resultados["id_processo"],
                        "regiao": regiao,
                    })

                self.print_msg(
                    message=message,
                    type_log=type_log,
                    row=row,
                )

        except Exception as e:
            tqdm.write("\n".join(traceback.format_exception(e)))
            self.print_msg(
                message="Erro ao extrair informações do processo",
                type_log="error",
                row=row,
            )

    def outras_informacoes(
        self,
        numero_processo: str,
        client: Client,
        id_processo: str,
        regiao: str,
        row: int,
    ) -> None:
        request_partes: Response = None
        request_assuntos: Response = None
        request_audiencias: Response = None

        data_partes: PartesJsonDict = None
        data_assuntos: list[AssuntoDict] = None
        data_audiencias: list[AudienciaDict] = None

        link_partes = el.LINK_CONSULTA_PARTES.format(
            trt_id=regiao,
            id_processo=id_processo,
        )
        link_assuntos = el.LINK_CONSULTA_ASSUNTOS.format(
            trt_id=regiao,
            id_processo=id_processo,
        )
        link_audiencias = el.LINK_AUDIENCIAS.format(
            trt_id=regiao,
            id_processo=id_processo,
        )

        sleep(0.25)
        with suppress(Exception):
            request_partes = client.get(url=link_partes)
            if request_partes:
                data_partes: PartesJsonDict = request_partes.json()
                self._salva_partes(
                    numero_processo=numero_processo,
                    data_partes=data_partes,
                )

        sleep(0.25)
        with suppress(Exception):
            request_assuntos = client.get(url=link_assuntos)
            if request_assuntos:
                data_assuntos = request_assuntos.json()
                self._salva_assuntos(
                    numero_processo=numero_processo,
                    data_assuntos=data_assuntos,
                )

        sleep(0.25)
        with suppress(Exception):
            request_audiencias = client.get(url=link_audiencias)
            if request_audiencias:
                data_audiencias = request_audiencias.json()
                self._salva_audiencias(
                    numero_processo=numero_processo,
                    data_audiencia=data_audiencias,
                )

    def _salva_audiencias(
        self,
        numero_processo: str,
        data_audiencia: list[AudienciaDict],
    ) -> None:
        if data_audiencia:
            list_audiencias: list[AudienciaProcessoPjeDict] = []

            list_audiencias.extend([
                AudienciaProcessoPjeDict(
                    ID_PJE=audiencia["id"],
                    NUMERO_PROCESSO=numero_processo,
                    TIPO_AUDIENCIA=audiencia["tipo"]["descricao"],
                    MODO_AUDIENCIA="PRESENCIAL"
                    if audiencia["tipo"]["isVirtual"]
                    else "VIRTUAL",
                    STATUS=audiencia["status"],
                    DATA_INICIO=audiencia.get("dataInicio"),
                    DATA_FIM=audiencia.get("dataFim"),
                    DATA_MARCACAO=audiencia.get("dataMarcacao"),
                )
                for audiencia in data_audiencia
            ])

            self.to_add_audiencias.extend(list_audiencias)

    def _salva_assuntos(
        self,
        numero_processo: str,
        data_assuntos: list[ItemAssuntoDict],
    ) -> AssuntosProcessoPJeDict | None:
        list_assuntos: list[AssuntosProcessoPJeDict] = []
        if data_assuntos:
            list_assuntos.extend([
                AssuntosProcessoPJeDict(
                    ID_PJE=assunto["id"],
                    PROCESSO=numero_processo,
                    ASSUNTO_COMPLETO=assunto["assunto"]["assuntoCompleto"],
                    ASSUNTO_RESUMIDO=assunto["assunto"]["assuntoResumido"],
                )
                for assunto in data_assuntos
            ])

            self.to_add_assuntos.extend(list_assuntos)

            return list_assuntos[-1]

        return None

    def _salva_partes(
        self,
        numero_processo: str,
        data_partes: PartesJsonDict,
    ) -> None:
        partes: list[PartesProcessoPJeDict] = []
        representantes: list[RepresentantePartesPJeDict] = []
        if data_partes:
            for v in data_partes.values():
                list_partes: list[ParteDict] = v

                for parte in list_partes:
                    partes.append(
                        PartesProcessoPJeDict(
                            ID_PJE=parte["id"],
                            NOME=parte["nome"],
                            DOCUMENTO=parte.get("documento", "000.000.000-00"),
                            TIPO_DOCUMENTO=parte.get(
                                "tipoDocumento",
                                "Não Informado",
                            ),
                            TIPO_PARTE=parte["polo"],
                            TIPO_PESSOA="Física"
                            if parte["tipoPessoa"].lower() == "f"
                            else "Jurídica",
                            PROCESSO=numero_processo,
                            POLO=parte["polo"],
                            PARTE_PRINCIPAL=parte["principal"],
                        ),
                    )

                    if "representantes" in parte:
                        representantes.extend(
                            [
                                RepresentantePartesPJeDict(
                                    ID_PJE=representante["id"],
                                    PROCESSO=numero_processo,
                                    NOME=representante["nome"],
                                    DOCUMENTO=representante["documento"],
                                    TIPO_DOCUMENTO=representante[
                                        "tipoDocumento"
                                    ],
                                    REPRESENTADO=parte["nome"],
                                    TIPO_PARTE=representante["polo"],
                                    TIPO_PESSOA=representante["tipoPessoa"],
                                    POLO=representante["polo"],
                                    OAB=representante.get("numeroOab", "0000"),
                                    EMAILS=",".join(
                                        representante["emails"]
                                        if "emails" in representantes
                                        else [],
                                    ),
                                    TELEFONE=f"({representante['dddCelular']}) {representante['numeroCelular']}"
                                    if "dddCelular" in representante
                                    and "numeroCelular" in representante
                                    else "",
                                )
                                for representante in parte["representantes"]
                            ],
                        )

            self.to_add_partes.extend(list_partes)
            self.to_add_representantes.extend(representantes)

    def capa_processual(
        self,
        result: ProcessoJudicialDict,
        regiao: str,
        row: int,
    ) -> None:
        """Formata o resultado da busca para armazenar na planilha."""
        link_consulta = f"https://pje.trt{regiao}.jus.br/pjekz/processo/{result['id']}/detalhe"

        dict_salvar_planilha = CapaProcessualPJeDict(
            ID_PJE=result["id"],
            LINK_CONSULTA=link_consulta,
            NUMERO_PROCESSO=result["numero"],
            CLASSE=result["classeJudicial"]["descricao"],
            SIGLA_CLASSE=result["classeJudicial"]["sigla"],
            ORGAO_JULGADOR=result["orgaoJulgador"]["descricao"],
            SIGLA_ORGAO_JULGADOR=result["orgaoJulgador"]["sigla"],
            DATA_DISTRIBUICAO=formata_tempo(result["distribuidoEm"])
            if "distribuidoEm" in result
            else "",
            STATUS_PROCESSO=result["labelStatusProcesso"],
            SEGREDO_JUSTIÇA=result["segredoDeJustica"],
            VALOR_CAUSA=result["valorDaCausa"],
        )

        self.to_add_processos.append(dict_salvar_planilha)

    def copia_integral(self) -> None:
        """Realiza o download da cópia integral do processo e salva no storage."""
        while True:
            setted_event = self.event_stop_bot.is_set()
            empty_queue = self.queue_files.unfinished_tasks == 0

            if setted_event and empty_queue:
                break

            try:
                data = self.queue_files.get()
                if data:
                    data = dict(data)
                    file_name: str = data.get("file_name")
                    row: int = data.get("row")
                    processo: str = data.get("processo")
                    client: Client = data.get("client")
                    id_processo: str = data.get("id_processo")
                    regiao: str = data.get("regiao")

                    self.print_msg(
                        message=f"Baixando arquivo do processo n.{processo}",
                        type_log="log",
                        row=row,
                    )

                    sleep(0.50)
                    headers = client.headers
                    cookies = client.cookies

                    client = Client(
                        timeout=900,
                        headers=headers,
                        cookies=cookies,
                    )
                    sleep(0.50)
                    link = el.LINK_DOWNLOAD_INTEGRA.format(
                        trt_id=regiao,
                        id_processo=id_processo,
                    )
                    message = f"Baixando arquivo do processo n.{processo}"
                    sleep(0.50)
                    self.print_msg(
                        message=message,
                        row=row,
                        type_log="log",
                    )

                    with client.stream("get", url=link) as response:
                        self.save_file_downloaded(
                            file_name=file_name,
                            response_data=response,
                            processo=processo,
                            row=row,
                        )

            except ExecutionError as e:
                self.print_msg(
                    message="\n".join(traceback.format_exception(e)),
                    row=row,
                    type_log="info",
                )

                msg = "Erro ao baixar arquivo"
                self.print_msg(message=msg, row=row, type_log="info")

            finally:
                self.queue_files.task_done()

    def save_file_downloaded(
        self,
        file_name: str,
        response_data: Response,
        processo: str,
        row: int,
    ) -> None:
        """Envia o `arquivo baixado` no processo para o `storage`.

        Arguments:
            file_name (str): Nome do arquivo.
            response_data (Response): response da request httpx.
            processo (str): processo.
            row (int): row do loop.

        """
        try:
            path_temp = workdir.joinpath("temp", self.pid.upper())

            path_temp.mkdir(parents=True, exist_ok=True)

            sleep_time = secrets.randbelow(7) + 2
            sleep(sleep_time)

            chunk = 8 * 1024 * 1024
            file_path = path_temp.joinpath(file_name)
            # Salva arquivo em chunks no storage
            with file_path.open("wb") as f:
                for _bytes in response_data.iter_bytes(chunk):
                    sleep(0.5)
                    f.write(_bytes)

            """
            >>> with suppress(Exception):
            >>>     other_path_ = Path(environ["PATH_SRV"])
            >>>     with other_path_.joinpath(file_name).open("wb") as f:
            >>>         for _bytes in response_data.iter_bytes(chunk):
            >>>             sleep(0.5)
            >>>             f.write(_bytes)
            """

        except (FileUploadError, Exception) as e:
            str_exc = "\n".join(traceback.format_exception_only(e))
            message = "Não foi possível baixar o arquivo. " + str_exc
            self.print_msg(
                row=row,
                message=message,
                type_log="info",
            )

        finally:
            message = f"Arquivo do processo n.{processo} baixado com sucesso!"
            self.print_msg(
                row=row,
                message=message,
                type_log="success",
            )
