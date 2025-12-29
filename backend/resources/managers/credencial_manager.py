"""Gerenciador de credenciais CrawJUD."""

from __future__ import annotations

from base64 import b64decode
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path

    from backend.task_manager.controllers.head import CrawJUD

type AnyType = any


class CredencialManager:
    """Gerenciador de credenciais CrawJUD."""

    _username: str = None
    _password: str = None

    _certificado: Path = None
    _kdbx: Path = None

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
        self._otp = config.get("otp")

        if config.get("certificado"):
            self._certificado_nome = config.get("nome_certificado")
            self._certificado_bytes = b64decode(config.get("certificado"))

    @property
    def username(self) -> str:
        """Retorne o nome de usuário carregado."""
        return self._username

    @property
    def password(self) -> str:
        """Retorne a senha carregada."""
        return self._password

    @property
    def certificado(self) -> Path:

        if not self._certificado:
            path_execucao = self.bot.output_dir_path
            path_certificado = path_execucao.joinpath(self._certificado_nome)
            path_certificado.write_bytes(self._certificado_bytes)
            self._certificado = path_certificado

        return self._certificado

    @property
    def otp(self) -> str:

        return self._otp
