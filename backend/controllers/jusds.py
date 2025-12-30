"""Módulo para a classe de controle dos robôs Elaw."""

from __future__ import annotations

from typing import TYPE_CHECKING as TYPE_CHECKING

from backend.controllers.head import CrawJUD
from backend.resources.auth import AutenticadorElaw
from backend.resources.search import ElawSearch


class JusDsBot(CrawJUD):
    """Classe de controle para robôs do Elaw."""

    def __init__(self) -> None:
        """Inicialize o robô Elaw."""
        self.search = ElawSearch(self)
        self.auth = AutenticadorElaw(self)
