from __future__ import annotations

from typing import ClassVar, TypedDict

from backend.common import raise_password_token
from backend.common.exceptions import ExecutionError, FileError
from backend.controllers import PJeBot
from backend.controllers.projudi import ProjudiBot
from backend.interfaces import BotData, DataSucesso
from backend.resources import RegioesIterator
from backend.resources.driver.web_element import WebElement
from backend.resources.elements import projudi as el
from backend.resources.formatadores import formata_string

__all__ = [
    "BotData",
    "DataSucesso",
    "ExecutionError",
    "FileError",
    "ProjudiBot",
    "WebElement",
    "el",
    "formata_string",
    "raise_password_token",
]


class HabilitacaoDict(TypedDict):
    NUMERO_PROCESSO: str
    PETICAO_PRINCIPAL: str
    ANEXOS: str


class HabilitacaoPJe(PJeBot):
    name: ClassVar[str] = "pje_habilitacao"

    def execution(self) -> None:
        generator_regioes = RegioesIterator[HabilitacaoDict](self)
        self.total_rows = len(self.posicoes_processos)

        for data_regiao in generator_regioes:
            if self.bot_stopped.is_set():
                break

            if not self.auth():
                continue
            self.queue_regiao(data=data_regiao)

        self.finalizar_execucao()

    def queue_regiao(self, data: list[HabilitacaoDict]) -> None:
        """Enfileire processos judiciais para processamento.

        Args:
            data (list[BotData]): Lista de dados dos processos.

        """
        for processo_data in data:
            self.bot_data = processo_data
