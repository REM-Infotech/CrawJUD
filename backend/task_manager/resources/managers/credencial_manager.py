"""Gerenciador de credenciais CrawJUD."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable

    from backend.task_manager.controllers.head import CrawJUD

type AnyType = any


class ClassProperty:
    """Implemente um descriptor para criar propriedades de classe.

    Args:
        func (Callable): Função que será usada como propriedade de classe.

    """

    def __init__(self, func: Callable) -> None:  # noqa: D107
        self.func = func

    def __get__[T](self, instance: AnyType, owner: AnyType) -> T:  # noqa: D105
        return self.func(owner)


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
        self._username = config.get("username")
        self._password = config.get("password")

        self._senha_kdbx = config.get("senha_kdbx")
        self._senha_certificado = config.get("senha_certificado")

    @ClassProperty
    def username(self) -> str:
        """Retorne o nome de usuário carregado."""
        return self._username

    @ClassProperty
    def password(self) -> str:
        """Retorne a senha carregada."""
        return self._password

    @ClassProperty
    def senha_kdbx(self) -> str:
        return self._senha_kdbx

    @ClassProperty
    def senha_certificado(self) -> str:
        return self._senha_certificado
