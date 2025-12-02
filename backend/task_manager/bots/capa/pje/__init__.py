"""Módulo do robô de capa do PJe."""

from __future__ import annotations

import traceback
from concurrent.futures import Future, ThreadPoolExecutor
from time import sleep
from typing import TYPE_CHECKING, ClassVar, TypedDict

from httpx import Client
from tqdm import tqdm

from backend.task_manager.bots.capa.pje._timeline import TimeLinePJe
from backend.task_manager.common.exceptions import ExecutionError as ExecutionError
from backend.task_manager.controllers.pje import PJeBot
from backend.task_manager.interfaces.pje import (
    CapaPJe,
)
from backend.task_manager.resources import RegioesIterator
from backend.task_manager.resources.queues.file_downloader import FileDownloader

if TYPE_CHECKING:
    from queue import Queue

    from backend.task_manager.interfaces import BotData
    from backend.task_manager.types_app import AnyType as AnyType
    from backend.task_manager.types_app import Dict


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
        cookies = self.auth.get_cookies()
        client_context = Client(cookies=cookies)
        thread_pool = ThreadPoolExecutor(4)

        with client_context as client, thread_pool as pool:
            futures: list[Future[None]] = []
            for item in data:
                futures.append(
                    pool.submit(self.queue, item=item, client=client),
                )
                sleep(10)

    def queue(self, item: BotData, client: Client) -> None:
        """Enfileire e processe um processo judicial PJE.

        Args:
            item (BotData): Dados do processo.
            client (Client): Cliente HTTP autenticado.

        """
        if not self.bot_stopped.is_set():
            sleep(0.5)
            row = int(
                self.posicoes_processos[item["NUMERO_PROCESSO"]] + 1,
            )
            processo = item["NUMERO_PROCESSO"]
            try:
                resultados = self.search(
                    data=item,
                    row=row,
                    client=client,
                )
                if not resultados:
                    return

                self.print_message(
                    message="Processo encontrado!",
                    message_type="info",
                    row=row,
                )

                capa = self.capa_processual(
                    result=resultados["data_request"],
                )
                id_processo = resultados["id_processo"]
                timeline = TimeLinePJe.load(
                    processo=processo,
                    cliente=client,
                    id_processo=id_processo,
                    regiao=self.regiao,
                    bot=self,
                )

                for file in timeline.documentos:
                    if not any(
                        [
                            "acórdão" in file["tipo"].lower(),
                            "acordao" in file["tipo"].lower(),
                            "acordo" in file["tipo"].lower(),
                            "sentença" in file["tipo"].lower(),
                        ],
                    ):
                        continue

                    timeline.baixar_documento(
                        bot=self,
                        documento=file,
                        grau="1",
                        inclur_assinatura=True,
                    )

                sleep(0.5)

                self.append_success(
                    worksheet="Resultados",
                    data_save=[capa],
                )

                message_type = "success"
                message = "Execução Efetuada com sucesso!"
                self.print_message(
                    message=message,
                    message_type=message_type,
                    row=row,
                )

            except Exception as e:
                exc = "\n".join(traceback.format_exception(e))
                tqdm.write(exc)
                self.print_message(
                    message="Erro ao extrair informações do processo",
                    message_type="error",
                    row=row,
                )

    def capa_processual(self, result: Dict) -> CapaPJe:
        """Gere a capa processual do processo judicial PJE.

        Args:
            result (ProcessoJudicialDict): Dados do processo judicial.

        Returns:
            CapaPJe: Dados da capa processual gerados.

        """
        link_consulta = f"https://pje.trt{self.regiao}.jus.br/pjekz/processo/{result['id']}/detalhe"
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
