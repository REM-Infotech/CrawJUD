"""Módulo do robô de capa do PJe."""

from __future__ import annotations

import traceback
from concurrent.futures import Future, ThreadPoolExecutor
from time import sleep
from typing import TYPE_CHECKING, ClassVar, TypedDict

from httpx import Client
from tqdm import tqdm

from backend.common.exceptions import (
    ExecutionError as ExecutionError,
)
from backend.common.exceptions._fatal import FatalError
from backend.controllers.pje import PJeBot
from backend.interfaces.pje import (
    CapaPJe,
)
from backend.resources import RegioesIterator
from backend.resources.queues.file_downloader import FileDownloader
from backend.task_manager.bots.capa.pje._timeline import TimeLinePJe

if TYPE_CHECKING:
    from queue import Queue

    from backend.interfaces import BotData
    from backend.types_app import AnyType as AnyType
    from backend.types_app import Dict


class ArgumentosPJeCapa(TypedDict):
    NUMERO_PROCESSO: str
    GRAU: str
    REGIAO: str


class Capa(PJeBot):
    """Gerencie autenticação e processamento de processos PJE."""

    queue_files: Queue
    name: ClassVar[str] = "capa_pje"

    def execution(self) -> None:
        """Execute o processamento dos processos judiciais PJE."""
        self.download_file = FileDownloader()
        generator_regioes = RegioesIterator[ArgumentosPJeCapa](bot=self)

        self.total_rows = len(self.posicoes_processos)

        for data_regiao in generator_regioes:
            if self.bot_stopped.is_set():
                break

            if not self.auth():
                continue

            self.queue_regiao(data=data_regiao)
        self.finalizar_execucao()

    def queue_regiao(self, data: list[BotData]) -> None:
        """Enfileire processos judiciais para processamento.

        Args:
            data (list[BotData]): Lista de dados dos processos.

        """
        url = f"https://pje.trt{self.regiao}.jus.br/pjekz"
        cookies = self.auth.get_cookies()
        headers = self.auth.get_headers(url=url)
        client_context = Client(cookies=cookies, headers=headers)
        thread_pool = ThreadPoolExecutor(2)

        with client_context as client, thread_pool as pool:
            futures: list[Future[None]] = []
            for item in data:
                if self.bot_stopped.is_set():
                    break

                futures.append(
                    pool.submit(self.queue, item=item, client=client),
                )
                sleep(5)

    def queue(self, item: BotData, client: Client) -> None:
        """Enfileire e processe um processo judicial PJE.

        Args:
            item (BotData): Dados do processo.
            client (Client): Cliente HTTP autenticado.

        """

        processo = item["NUMERO_PROCESSO"]
        pos_processo = self.posicoes_processos[processo]
        termos: str = item.get("TERMOS", "SENTENÇA,ACÓRDAO,LIMINAR")
        if not termos:
            return

        row = int(pos_processo) + 1
        if not self.bot_stopped.is_set():
            sleep(0.5)

            try:
                resultados = self.search(
                    data=item,
                    row=row,
                    client=client,
                )
                if resultados:
                    self.print_message(
                        message="Processo encontrado!",
                        message_type="info",
                        row=row,
                    )

                    id_processo = resultados["id_processo"]
                    data_ = resultados["data_request"]

                    termos: list[str] = termos.split(",") if ", " in termos else [termos]

                    capa = self.capa_processual(result=data_)
                    timeline = TimeLinePJe.load(
                        processo=processo,
                        cliente=client,
                        id_processo=id_processo,
                        regiao=self.regiao,
                        bot=self,
                    )

                    for file in timeline.documentos:
                        if any(
                            termo.lower() in file["tipo"].lower() for termo in termos
                        ):
                            timeline.baixar_documento(
                                bot=self,
                                documento=file,
                                grau="1",
                                inclur_assinatura=True,
                            )

                        self.append_success(
                            worksheet="Resultados",
                            data_save=[capa],
                        )

                        return

                    type_ = "success"
                    msg_ = "Execução Efetuada com sucesso!"
                    self.print_message(msg_, type_, row)
                    item.update({"MENSAGEM_ERRO": msg_})
                    self.append_error(data_save=item)

            except Exception as e:
                exc = "\n".join(traceback.format_exception(e))
                tqdm.write(exc)
                self.print_message(
                    message="Erro ao extrair informações do processo",
                    message_type="error",
                    row=row,
                )

                raise FatalError(e) from e

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
