"""Gerenciador de credenciais CrawJUD."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from backend.task_manager.controllers.head import CrawJUD


class CredencialManager:
    """Gerenciador de credenciais CrawJUD."""

    _username: str = None

    def __init__(self, bot: CrawJUD) -> None:
        """Instancia da gestão de credenciais."""
        self.bot = bot

    def load_credenciais(self, config: dict[str, str]) -> None:
        """Carregue credenciais do dicionário de configuração.

        Args:
            config (dict): Dicionário com usuário e senha.

        """
        self._username = config["username"]
        self._password = config["password"]

    @property
    def username(self) -> str:
        """Retorne o nome de usuário carregado."""
        return self._username

    @property
    def password(self) -> str:
        """Retorne a senha carregada."""
        return self._password
