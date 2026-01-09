"""Módulo para a classe de controle dos robôs Elaw."""

from __future__ import annotations

from typing import TYPE_CHECKING as TYPE_CHECKING
from typing import ClassVar

from backend.controllers import CrawJUD
from backend.resources.auth.jusds import AutenticadorJusds
from backend.resources.search.jusds import JusdsSearch


class JusdsBot(CrawJUD):
    """Classe de controle para robôs do Elaw."""

    _main_window: ClassVar[str] = ""
    _window_busca_processo: ClassVar[str] = ""

    def __init__(self) -> None:
        """Inicialize o robô Elaw."""
        self.search = JusdsSearch(self)
        self.auth = AutenticadorJusds(self)
        super().__init__()

    @property
    def main_window(self) -> str:
        return self._main_window

    @main_window.setter
    def main_window(self, val: str) -> None:
        self._main_window = val

    @property
    def window_busca_processo(self) -> str:
        return self._window_busca_processo

    @window_busca_processo.setter
    def window_busca_processo(self, val: str) -> None:
        self._window_busca_processo = val
