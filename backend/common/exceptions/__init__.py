"""Módulo de tratamento de exceptions do robô."""

from __future__ import annotations

import traceback
from typing import TYPE_CHECKING, ClassVar, Literal, NoReturn, Self

if TYPE_CHECKING:
    from typings import Any

MessageError = "Erro ao executar operaçao: "
type MessageTokenError = Literal["Senha do Token Incorreta"]


def formata_msg(exc: Exception | None = None) -> str:
    """Formata mensagem de erro detalhada a partir de uma exceção fornecida ao bot.

    Args:
        exc (Exception | None): Exceção a ser formatada, se fornecida.

    Returns:
        str: Mensagem formatada contendo detalhes da exceção, se houver.

    """
    if exc:
        return "\n Exception: " + "\n".join(
            traceback.format_exception_only(exc),
        )

    return ""


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
        super().__init__(self.message)

    def __str__(self) -> str:
        """Retorne a mensagem de erro formatada.

        Returns:
            str: Mensagem de erro com detalhes da exceção.

        """
        return self.message

    def __repr__(self) -> str:
        """Return the string representation of the FatalError for debugging."""
        return f"{self.__class__.__name__}(type={self._exc_type}, message={self._exc_msg})"

    def __reduce__(self) -> tuple[type[Self], tuple[Exception]]:  # noqa: D105
        # Provide a way for pickle to reconstruct the object
        return (
            self.__class__,
            (Exception(self._exc_msg),),  # reconstruct with a generic Exception
        )

    def __getstate__(self) -> dict[str, Any]:  # noqa: D105
        # Only store pickleable attributes
        return {
            "_exc_str": self._exc_str,
            "_exc_type": self._exc_type,
            "_exc_msg": self._exc_msg,
            "_traceback": self._traceback,
            "message": self.message,
        }

    def __setstate__(self, state: dict[str, Any]) -> None:  # noqa: D105
        self._exc_str = state["_exc_str"]
        self._exc_type = state["_exc_type"]
        self._exc_msg = state["_exc_msg"]
        self._traceback = state["_traceback"]
        self.message = state["message"]


class StartError(BaseCrawJUDError):
    """Exception raised for errors that occur during the start of the bot."""


def raise_start_error(message: str) -> NoReturn:
    """Lança exceção StartError com mensagem personalizada fornecida.

    Args:
        message (str): Mensagem de erro a ser exibida na exceção.

    Raises:
        StartError: Exceção lançada com a mensagem informada.

    """
    raise StartError(message=message)


class DriverNotCreatedError(BaseCrawJUDError):
    """Handler de erro de inicialização do WebDriver."""


class AuthenticationError(BaseCrawJUDError):
    """Handler de erro de autenticação."""

    def __init__(self, message: str = "Erro de autenticação.") -> None:
        """Inicializa a mensagem de erro."""
        super().__init__(message)


class BaseExceptionCeleryAppError(Exception):
    """Base exception class for Celery app errors."""


class BotNotFoundError(AttributeError):
    """Exceção para indicar que o robô especificado não foi encontrado.

    Args:
        message (str): Mensagem de erro.

    Returns:
        None

    Raises:
        AttributeError: Sempre que o robô não for localizado.

    """

    def __init__(
        self,
        message: str,
        name: str | None = None,
        obj: object | None = None,
    ) -> None:
        """Inicializa a exceção BotNotFoundError.

        Args:
            message (str): Mensagem de erro.
            name (str | None): Nome do robô, se disponível.
            obj (object | None): Objeto relacionado ao erro, se disponível.



        """
        self.name = name
        self.obj = obj
        super().__init__(message)


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

        # Chama Exception.__init__ diretamente para evitar reformatação
        Exception.__init__(self, self.message)


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
    "BotNotFoundError",
    "DriverNotCreatedError",
    "ExecutionError",
]
