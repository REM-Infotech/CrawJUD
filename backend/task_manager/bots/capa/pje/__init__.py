"""Módulo do robô de capa do PJe."""

from __future__ import annotations

import traceback
from time import sleep
from typing import TYPE_CHECKING, ClassVar

from tqdm import tqdm

from backend.common.exceptions import (
    ExecutionError as ExecutionError,
)
from backend.common.exceptions._fatal import FatalError
from backend.controllers.pje import PJeBot
from backend.dicionarios import CapaPJe
from backend.resources import RegioesIterator as RegioesIterator

from ._assuntos import AssuntosPJe
from ._audiencias import AudienciasPJe
from ._partes import PartesPJe
from ._timeline import TimeLinePJe

if TYPE_CHECKING:
    from queue import Queue

    from httpx import Client

    from backend.dicionarios import PJeCapa
    from backend.types_app import Dict


class Capa(PJeBot):
    """Gerencie autenticação e processamento de processos PJE."""

    queue_files: Queue
    name: ClassVar[str] = "capa_pje"

    def queue(self, item: PJeCapa, client: Client) -> None:
        """Enfileire e processe um processo judicial PJE.

        Args:
            item (PJeCapa): Dados do processo.
            client (Client): Cliente HTTP autenticado.

        """

        processo = item["NUMERO_PROCESSO"]
        pos_processo = self.posicoes_processos[processo]

        row = int(pos_processo) + 1
        if not self.bot_stopped.is_set():
            sleep(0.5)

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

                id_processo = resultados["id_processo"]
                data_ = resultados["data_request"]
                self.append_success("Capa", [self.capa_processual(result=data_)])

                if str(item.get("TRAZER_ASSUNTOS", "sim")).lower() == "sim":
                    assuntos = AssuntosPJe.extrair(
                        cliente=client,
                        regiao=self.regiao,
                        id_processo=id_processo,
                        processo=processo,
                    )
                    self.append_success("Assuntos", assuntos)

                if str(item.get("TRAZER_AUDIENCIAS", "sim")).lower() == "sim":
                    audiencias = AudienciasPJe.extrair(
                        cliente=client,
                        regiao=self.regiao,
                        id_processo=id_processo,
                        processo=processo,
                    )
                    self.append_success("Audiências", audiencias)

                if str(item.get("TRAZER_PARTES", "sim")).lower() == "sim":
                    partes_cls = PartesPJe.extrair(
                        cliente=client,
                        regiao=self.regiao,
                        id_processo=id_processo,
                        processo=processo,
                    )
                    if partes_cls:
                        self.append_success("Partes", partes_cls.formata_partes())

                        representantes = partes_cls.formata_representantes()
                        self.append_success("Representantes", representantes)

                if str(item.get("TRAZER_MOVIMENTACOES", "sim")).lower() == "sim":
                    tl = TimeLinePJe.load(
                        bot=self,
                        cliente=client,
                        id_processo=id_processo,
                        regiao=self.regiao,
                        processo=processo,
                        apenas_assinados=False,
                    )

                    if tl.result:
                        self.append_success("Movimentações", tl.movimentacoes)

                type_ = "success"
                msg_ = "Execução Efetuada com sucesso!"
                self.print_message(msg_, type_, row)

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
        id_ = result["id"]
        reg = self.regiao
        link_consulta = f"https://pje.trt{reg}.jus.br/pjekz/processo/{id_}/detalhe"
        return CapaPJe(
            ID_PJE=id_,
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
