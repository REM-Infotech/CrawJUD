from __future__ import annotations

from typing import TypedDict


class HealtCheck(TypedDict):
    """Defina informações de status do sistema para verificação.

    Args:
        status (str): Situação geral do sistema.
        database (str): Situação do banco de dados.
        timestamp (str): Data e hora da verificação.

    """

    status: str
    database: str
    timestamp: str


class LoginForm(TypedDict):
    """Defina dados de login do usuário para autenticação.

    Args:
        login (str): Nome de usuário.
        password (str): Senha do usuário.
        remember (bool): Se deve manter sessão ativa.

    """

    login: str
    password: str
    remember: bool
