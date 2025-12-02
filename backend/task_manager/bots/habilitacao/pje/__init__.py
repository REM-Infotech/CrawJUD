from __future__ import annotations

from typing import ClassVar, TypedDict

from backend.task_manager.common import raise_password_token
from backend.task_manager.common.exceptions import ExecutionError, FileError
from backend.task_manager.controllers import PJeBot
from backend.task_manager.controllers.projudi import ProjudiBot
from backend.task_manager.interfaces import BotData, DataSucesso
from backend.task_manager.resources import RegioesIterator
from backend.task_manager.resources.driver.web_element import WebElementBot
from backend.task_manager.resources.elements import projudi as el
from backend.task_manager.resources.formatadores import formata_string

__all__ = [
    "BotData",
    "DataSucesso",
    "ExecutionError",
    "FileError",
    "ProjudiBot",
    "WebElementBot",
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
