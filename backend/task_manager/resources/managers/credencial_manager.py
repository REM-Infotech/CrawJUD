"""Gerenciador de credenciais CrawJUD."""

from __future__ import annotations

from typing import TYPE_CHECKING

from backend.task_manager.common.exceptions._file import (
    ArquivoNaoEncontradoError,
)

if TYPE_CHECKING:
    from collections.abc import Callable
    from pathlib import Path

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

        self._kdbx_nome = self.bot.config.get("kdbx")
        self._senha_kdbx = self.bot.config.get("senha_kdbx")

        self._cpf_cnpj_certificado = self.bot.config.get("cpf_cnpj_certificado")
        self._certificado_nome = self.bot.config.get("certificado")
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
    def certificado(self) -> Path:

        if not self._certificado:
            path_execucao = self.bot.output_dir_path
            certificado_ = path_execucao.joinpath(self._certificado_nome)

            if certificado_.exists():
                raise ArquivoNaoEncontradoError(
                    str(certificado_),
                    f'Arquivo "{certificado_.name}" não encontrado!',
                ) from None

            self._certificado = certificado_

        return self._certificado

    @ClassProperty
    def senha_certificado(self) -> str:
        return self._senha_certificado

    @ClassProperty
    def kdbx(self) -> Path:

        if not self._kdbx:
            path_execucao = self.bot.output_dir_path
            kdbx_ = path_execucao.joinpath(self._kdbx_nome)

            if kdbx_.exists():
                raise ArquivoNaoEncontradoError(
                    str(kdbx_),
                    f'Arquivo "{kdbx_.name}" não encontrado!',
                ) from None

            self._kdbx = kdbx_

        return self._kdbx

    @ClassProperty
    def senha_kdbx(self) -> str:
        return self._senha_kdbx

    @ClassProperty
    def cpf_cnpj_certificado(self) -> str:
        return self._cpf_cnpj_certificado
