from __future__ import annotations

import traceback
from concurrent.futures import Future, ThreadPoolExecutor
from contextlib import suppress
from time import sleep
from typing import TYPE_CHECKING

from httpx import Client
from tqdm import tqdm

from backend.controllers.pje import PJeBot
from backend.interfaces.pje import CapaPJe, DictResults
from backend.resources import RegioesIterator
from backend.resources.driver import BotDriver

from ._dicionarios import PJeMovimentacao
from ._timeline import TimeLinePJe

if TYPE_CHECKING:
    from queue import Queue

    from seleniumwire.webdriver import Chrome

    from backend.types_app import Dict

    from ._dicionarios import DocumentoPJe


THREAD_PREFIX = "Fila região {regiao}"
WORKERS_QTD = 4


class Movimentacao(PJeBot):
    queue_files: Queue
    name = "movimentacao_pje"
    driver: Chrome

    def execution(self) -> None:

        self.driver.quit()
        generator_regioes = RegioesIterator[PJeMovimentacao](bot=self)
        self.total_rows = len(self.posicoes_processos)

        for data_regiao in generator_regioes:
            self.bot_driver = BotDriver(self)

            if self.bot_stopped.is_set():
                break

            with suppress(Exception):
                if self.auth():
                    self.queue_regiao(data=data_regiao)

            self.driver.quit()

        self.finalizar_execucao()

    def queue_regiao(self, data: list[PJeMovimentacao]) -> None:
        """Enfileire processos judiciais para processamento.

        Args:
            data (list[PJeMovimentacao]): Lista de dados dos processos.

        """
        url = f"https://pje.trt{self.regiao}.jus.br/pjekz"
        cookies = self.auth.get_cookies()
        headers = self.auth.get_headers(url=url)
        client_context = Client(cookies=cookies, headers=headers)
        self.executor = ThreadPoolExecutor(WORKERS_QTD, THREAD_PREFIX)

        with client_context as client, self.executor as pool:
            futures: list[Future[None]] = []
            for item in data:
                if self.bot_stopped.is_set():
                    break

                futures.append(pool.submit(self.queue, item=item, client=client))
                sleep(2.5)

            _results = [future.result() for future in futures]

    def set_event(self) -> None:

        self.executor.shutdown(wait=False, cancel_futures=True)

    def queue(self, item: PJeMovimentacao, client: Client) -> None:
        """Enfileire e processe um processo judicial PJE.

        Args:
            item (PJeMovimentacao): Dados do processo.
            client (Client): Cliente HTTP autenticado.

        """
        processo = item["NUMERO_PROCESSO"]
        pos_processo = self.posicoes_processos[processo]
        termos: str = item.get("TERMOS", "")
        row = int(pos_processo) + 1
        self._is_grau_list = False
        if self.bot_stopped.is_set() or not termos:
            return

        try:
            grau = str(item.get("GRAU", "1"))
            kw = {"item": item, "row": row, "client": client, "termos": termos}

            if "," in grau:
                grau = grau.replace(" ", "").split(",")
                self._is_grau_list = True
                for g in grau:
                    msg_ = f"Buscando proceso na {g}a instância"
                    m_type = "log"
                    kw.update({"grau": g})
                    self.print_message(msg_, m_type, row)

                    client.headers.update({"X-Grau-Instancia": g})

                    self.extrair_processo(**kw)
                return

            kw.update({"grau": grau})
            client.headers.update({"x-grau-instancia": grau})
            self.extrair_processo(**kw)

        except Exception as e:
            exc = "\n".join(traceback.format_exception(e))
            tqdm.write(exc)
            self.print_message(
                message="Erro ao extrair informações do processo",
                message_type="error",
                row=row,
            )
            raise

    def extrair_processo(
        self,
        item: PJeMovimentacao,
        row: int,
        client: Client,
        termos: list[str],
        grau: str,
    ) -> None:
        sleep(1.5)
        kw = {"data": item, "row": row, "client": client}
        resultados = self.search(**kw)
        if resultados:
            self.print_message(
                message="Processo encontrado!",
                message_type="info",
                row=row,
            )

            kw_tl = self.kw_timeline(resultados, item, client)
            sleep(2.5)
            timeline = TimeLinePJe.load(**kw_tl)

            termos: list[str] = self.formata_termos(termos)
            arquivos = self.filtrar_arquivos(timeline, termos)
            capa = self.capa_processual(result=resultados["data_request"])

            for file in arquivos:
                if self.bot_stopped.is_set():
                    break

                kw_dw = {
                    "documento": file,
                    "grau": grau,
                    "inclur_assinatura": True,
                    "row": row,
                }
                timeline.baixar_documento(**kw_dw)
                sleep(0.5)

            if len(arquivos) == 0:
                self.salva_erro(row=row, item=item)
                sleep(2.5)
                return

            sleep(0.5)
            type_ = "success"
            msg_ = "Execução efetuada com sucesso!"
            self.print_message(msg_, type_, row)
            self.append_success(
                worksheet="Resultados",
                data_save=[capa],
            )

    def kw_timeline(
        self,
        result: DictResults,
        item: PJeMovimentacao,
        client: Client,
    ) -> dict:

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

    def salva_erro(self, row: int, item: PJeMovimentacao) -> None:

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
