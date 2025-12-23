from __future__ import annotations

import traceback
from concurrent.futures import Future, ThreadPoolExecutor
from contextlib import suppress
from threading import Semaphore
from time import sleep
from typing import TYPE_CHECKING, ClassVar, TypedDict

from httpx import Client
from tqdm import tqdm

from backend.common.exceptions import (
    ExecutionError as ExecutionError,
)
from backend.interfaces.pje import (
    CapaPJe,
    DictResults,
)
from backend.task_manager.controllers.pje import PJeBot
from backend.task_manager.resources import RegioesIterator
from backend.task_manager.resources.queues.file_downloader import FileDownloader

from ._timeline import TimeLinePJe

if TYPE_CHECKING:
    from queue import Queue

    from backend.interfaces import BotData
    from backend.types_app import AnyType as AnyType
    from backend.types_app import Dict

    from ._dicionarios import DocumentoPJe


class ArgumentosPJeCapa(TypedDict):
    NUMERO_PROCESSO: str
    GRAU: str
    REGIAO: str


class Movimentacao(PJeBot):
    queue_files: Queue
    name: ClassVar[str] = "movimentacao_pje"

    def execution(self) -> None:
        self.download_file = FileDownloader()
        self.semaforo = Semaphore(1)

        generator_regioes = RegioesIterator[ArgumentosPJeCapa](bot=self)
        self.total_rows = len(self.posicoes_processos)

        for data_regiao in generator_regioes:
            if self.bot_stopped.is_set():
                break

            with suppress(Exception):
                if self.auth():
                    self.queue_regiao(data=data_regiao)

        self.finalizar_execucao()

    def queue_regiao(self, data: list[BotData]) -> None:
        """Enfileire processos judiciais para processamento.

        Args:
            data (list[BotData]): Lista de dados dos processos.

        """
        sleep(5)
        cookies = self.auth.get_cookies()

        url = f"https://pje.trt{self.regiao}.jus.br/pjekz"
        requests = self.driver.requests
        headers_ = filter(lambda x: x.url.startswith(url), requests)
        cookies = self.auth.get_cookies()
        headers = dict(list(headers_)[-1].headers.items())
        client_context = Client(cookies=cookies, headers=headers)

        thread_pool = ThreadPoolExecutor(
            max_workers=4,
            thread_name_prefix=f"Fila região {self.regiao}",
        )

        with client_context as client, thread_pool as pool:
            futures: list[Future[None]] = [
                pool.submit(self.queue, item=item, client=client) for item in data
            ]

            _results = [future.result() for future in futures]

    def queue(self, item: BotData, client: Client) -> None:
        """Enfileire e processe um processo judicial PJE.

        Args:
            item (BotData): Dados do processo.
            client (Client): Cliente HTTP autenticado.

        """
        with self.semaforo:
            processo = item["NUMERO_PROCESSO"]
            pos_processo = self.posicoes_processos[processo]
            termos: str = item.get("TERMOS", "")
            row = int(pos_processo) + 1
            if self.bot_stopped.is_set() or not termos:
                return

            sleep(1.5)

            try:
                kw = {"data": item, "row": row, "client": client}
                resultados = self.search(**kw)
                if resultados:
                    self.print_message(
                        message="Processo encontrado!",
                        message_type="info",
                        row=row,
                    )

                    sleep(1.5)
                    kw_tl = self.kw_timeline(resultados, item, client)
                    timeline = TimeLinePJe.load(**kw_tl)

                    termos: list[str] = self.formata_termos(termos)
                    arquivos = self.filtrar_arquivos(timeline, termos)
                    capa = self.capa_processual(result=resultados["data_request"])

                    sleep(1.5)

                    for file in arquivos:
                        kw_dw = {
                            "documento": file,
                            "grau": "1",
                            "inclur_assinatura": True,
                        }
                        timeline.baixar_documento(**kw_dw)

                    if len(arquivos) == 0:
                        self.salva_erro(row=row, item=item)
                        return

                    type_ = "success"
                    msg_ = "Execução Efetuada com sucesso!"
                    self.print_message(msg_, type_, row)
                    self.append_success(
                        worksheet="Resultados",
                        data_save=[capa],
                    )

                    sleep(1.5)

            except Exception as e:
                exc = "\n".join(traceback.format_exception(e))
                tqdm.write(exc)
                self.print_message(
                    message="Erro ao extrair informações do processo",
                    message_type="error",
                    row=row,
                )
                raise

    def kw_timeline(self, result: DictResults, item: BotData, client: Client) -> dict:

        processo = item["NUMERO_PROCESSO"]
        return {
            "processo": processo,
            "cliente": client,
            "id_processo": result["id_processo"],
            "regiao": self.regiao,
            "bot": self,
        }

    def formata_termos(self, termos: str) -> list[str]:

        return termos.replace(", ", ",").split(",") if ", " in termos else [termos]

    def filtrar_arquivos(self, tl: TimeLinePJe, termos: list[str]) -> list[DocumentoPJe]:
        def termo_in_tipo(file: DocumentoPJe) -> bool:
            return any(termo.lower() in file["tipo"].lower() for termo in termos)

        return list(filter(termo_in_tipo, tl.documentos))

    def salva_erro(self, row: int, item: BotData) -> None:

        message = "Nenhum arquivo encontrado!"
        message_type = "error"

        item["MOTIVO_ERRO"] = message

        self.print_message(
            message=message,
            message_type=message_type,
            row=row,
        )
        self.append_error(data_save=[item])

    def capa_processual(self, result: Dict) -> CapaPJe:
        """Gere a capa processual do processo judicial PJE.

        Args:
            result (ProcessoJudicialDict): Dados do processo judicial.

        Returns:
            CapaPJe: Dados da capa processual gerados.

        """
        link_consulta = (
            f"https://pje.trt{self.regiao}.jus.br/pjekz/processo/{result['id']}/detalhe"
        )
        return CapaPJe(
            ID_PJE=result["id"],
            LINK_CONSULTA=link_consulta,
            processo=result["numero"],
            CLASSE=result["classeJudicial"]["descricao"],
            SIGLA_CLASSE=result["classeJudicial"]["sigla"],
            ORGAO_JULGADOR=result["orgaoJulgador"]["descricao"],
            SIGLA_ORGAO_JULGADOR=result["orgaoJulgador"]["sigla"],
            DATA_DISTRIBUICAO=result.get("distribuidoEm", ""),
            STATUS_PROCESSO=result["labelStatusProcesso"],
            SEGREDO_JUSTICA=result["segredoDeJustica"],
            VALOR_CAUSA=result["valorDaCausa"],
        )
