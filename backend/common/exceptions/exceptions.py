"""Módulo de tratamento de exceptions do robô."""

from __future__ import annotations

import traceback
from typing import ClassVar, Literal

from backend.resources.formatadores import formata_msg

MessageError = "Erro ao executar operaçao: "
type MessageTokenError = Literal["Senha do Token Incorreta"]


class BaseCrawJUDError(Exception):
    """Base exception class for CrawJUD-specific errors.

    Fornece formatação automática de mensagens de erro e
    integração com exceções aninhadas.
    """

    def __init__(
        self,
        message: str = MessageError,
        exc: Exception | None = None,
    ) -> None:
        """Inicialize a exceção com mensagem e exceção opcional.

        Args:
            message (str): Mensagem de erro principal.
            exc (Exception | None): Exceção original, se houver.

        """
        self.message = message + formata_msg(exc)
        Exception.__init__(self, self.message)


class ExecutionError(BaseCrawJUDError):
    """Exceção para erros de execução do robô."""

    def __init__(
        self,
        message: str = MessageError,
        exc: Exception | None = None,
    ) -> None:
        """Inicialize exceção de execução com formatação especial.

        Args:
            message (str): Mensagem de erro principal.
            exc (Exception | None): Exceção original capturada.

        """
        # Formatação especial para mensagem padrão com exceção completa
        if message == MessageError and exc:
            self.message = message + "\n".join(
                traceback.format_exception(exc),
            )
        else:
            self.message = message + formata_msg(exc)

        super().__init__(self.message, self)


class StartError(BaseCrawJUDError):
    """Exception raised for errors that occur during the start of the bot."""


class DriverNotCreatedError(BaseCrawJUDError):
    """Handler de erro de inicialização do WebDriver."""


class AuthenticationError(BaseCrawJUDError):
    """Handler de erro de autenticação."""


class BaseExceptionCeleryAppError(Exception):
    """Base exception class for Celery app errors."""


class LoginSystemError(BaseCrawJUDError):
    """Exceção para erros de login robô."""


class ProcNotFoundError(BaseCrawJUDError):
    """Exception de Processo não encontrado."""


class GrauIncorretoError(BaseCrawJUDError):
    """Exception de Grau Incorreto/Não informado."""


class SaveError(BaseCrawJUDError):
    """Exception para erros de salvamento de Formulários/Arquivos."""


class FileError(BaseCrawJUDError):
    """Exception para erros de envio de arquivos."""


class CadastroParteError(BaseCrawJUDError):
    """Exception para erros de cadastro de parte no Elaw."""


class MoveNotFoundError(BaseCrawJUDError):
    """Exception para erros de movimentações não encontradas."""


class PasswordError(BaseCrawJUDError):
    """Exception para erros de senha."""


class NotFoundError(BaseCrawJUDError):
    """Exceção para erros de execução do robô."""


class FileUploadError(BaseCrawJUDError):
    """Exception para erros de upload de arquivos."""


class PasswordTokenError(BaseCrawJUDError):
    """Handler de erro de senha de token Projudi."""

    message: ClassVar[str] = ""

    def __init__(
        self,
        message: MessageTokenError = "Senha do Token Incorreta",
    ) -> None:
        """Inicializa a mensagem de erro."""
        self.message = message
        super().__init__(message)


__all__ = [
    "AuthenticationError",
    "BaseCrawJUDError",
    "BaseExceptionCeleryAppError",
    "DriverNotCreatedError",
    "ExecutionError",
]
