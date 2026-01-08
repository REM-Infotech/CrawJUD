from __future__ import annotations

import traceback
from time import sleep
from typing import TYPE_CHECKING

from tqdm import tqdm

from backend.components import TimeLinePJe
from backend.controllers.pje import PJeBot
from backend.dicionarios import CapaPJe, MovimentacaoPJe

if TYPE_CHECKING:
    from queue import Queue

    from httpx import Client
    from seleniumwire.webdriver import Chrome

    from backend.dicionarios import DictResults, DocumentoPJe, PJeMovimentacao
    from typings import Dict


THREAD_PREFIX = "Fila região {regiao}"
WORKERS_QTD = 2


class Movimentacao(PJeBot):
    queue_files: Queue
    name = "movimentacao_pje"
    driver: Chrome

    def queue(self, item: PJeMovimentacao, client: Client) -> None:
        """Enfileire e processe um processo judicial PJE.

        Args:
            item (PJeMovimentacao): Dados do processo.
            client (Client): Cliente HTTP autenticado.

        """
        termos: str = item.get("TERMOS", "")
        processo = item["NUMERO_PROCESSO"]
        pos_processo = self.posicoes_processos[processo]
        row = int(pos_processo) + 1
        grau = str(item.get("GRAU", 1))
        try:
            sleep(1)
            kw = {
                "item": item,
                "grau": grau,
                "row": row,
                "client": client,
                "processo": processo,
                "termos": termos,
            }
            if "," in grau:
                grau = grau.replace(" ", "").split(",")
                self._is_grau_list = True
                for g in grau:
                    msg_ = f"Buscando proceso na {g}a instância"
                    m_type = "log"
                    self.print_message(msg_, m_type, row)
                    kw.update({"grau": g})
                    self.extrair_processo(**kw)

                return

            self.extrair_processo(**kw)
            sleep(1)

        except Exception as e:  # noqa: BLE001
            exc = "\n".join(traceback.format_exception(e))
            tqdm.write(exc)
            self.print_message(
                message="Erro ao extrair informações do processo",
                message_type="error",
                row=row,
            )

    def extrair_processo(
        self,
        item: PJeMovimentacao,
        grau: str,
        row: int,
        client: Client,
        processo: str,
        termos: list[str],
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
            kw_tl.update({"grau": grau})
            sleep(2.5)
            timeline = TimeLinePJe.load(**kw_tl)

            termos: list[str] = self.formata_termos(termos)
            arquivos = self.filtrar_arquivos(timeline, termos)
            movimentacoes = self.filtrar_movimentacoes(timeline, termos)
            capa = self.capa_processual(
                result=resultados["data_request"],
            )

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

            sleep(0.5)
            type_ = "success"
            msg_ = "Execução efetuada com sucesso!"
            self.print_message(msg_, type_, row)
            self.append_success(
                worksheet="Resultados",
                data_save=[capa],
            )

            if movimentacoes:
                self.append_success("Movimentações", movimentacoes)

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

    def filtrar_arquivos(
        self,
        tl: TimeLinePJe,
        termos: list[str],
    ) -> list[DocumentoPJe]:
        def termo_in_tipo(file: DocumentoPJe) -> bool:
            return any(termo.lower() in file["tipo"].lower() for termo in termos)

        return list(filter(termo_in_tipo, tl.documentos))

    def filtrar_movimentacoes(
        self,
        tl: TimeLinePJe,
        termos: list[str],
    ) -> list[MovimentacaoPJe]:

        def termo_in_tipo(mov: MovimentacaoPJe) -> bool:
            return any(termo.lower() in mov["titulo"].lower() for termo in termos)

        return list(filter(termo_in_tipo, tl.movimentacoes))

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
