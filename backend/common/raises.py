"""Forneça funções utilitárias para lançar exceções customizadas.

Este módulo contém funções para lançar erros específicos
relacionados à autenticação, execução e validação.
"""

from __future__ import annotations

from typing import NoReturn

from backend.task_manager.common.exceptions.validacao import (
    ValidacaoStringError,
)

from .exceptions import ExecutionError, PasswordTokenError


def raise_password_token() -> NoReturn:
    """Password token error.

    Raises:
        PasswordTokenError: PasswordTokenError

    """
    raise PasswordTokenError(message="Senha Incorreta!")


def raise_execution_error(
    message: str,
    exc: Exception | None = None,
) -> NoReturn:
    """Lance erro de execução com mensagem personalizada.

    Args:
        message (str): Mensagem de erro a ser exibida.
        exc (Exception): Exceção original capturada.

    Raises:
        ExecutionError: Erro de execução.

    """
    raise ExecutionError(message=message) from exc


def auth_error() -> NoReturn:
    """Lance erro de autenticação.

    Raises:
        ExecutionError: Erro de autenticação.

    """
    raise ExecutionError(message="Erro de autenticacao")


def value_error() -> NoReturn:
    """Lance erro de validação de valor informado.

    Raises:
        ValidacaoStringError: Valor não corresponde ao esperado.

    """
    raise ValidacaoStringError(
        message="Valor informado não corresponde ao valor esperado",
    )
