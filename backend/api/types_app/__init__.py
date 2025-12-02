"""Defina tipos e aliases para uso em todo o projeto.

Este módulo centraliza definições de tipos e aliases
para padronizar e facilitar o desenvolvimento.
"""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any, Literal, ParamSpec, TypedDict, TypeVar

AnyType = Any

P = ParamSpec("P", bound=AnyType)
T = TypeVar("T", bound=AnyType)


type Sistemas = Literal[
    "projudi",
    "elaw",
    "esaj",
    "pje",
    "jusds",
    "csi",
]
type MessageType = Literal["info", "log", "error", "warning", "success"]
type Methods = Literal[
    "GET",
    "POST",
    "PUT",
    "DELETE",
    "PATCH",
    "OPTIONS",
]
type ConfigNames = Literal[
    "DevelopmentConfig",
    "TestingConfig",
    "ProductionConfig",
]
type ModeMiddleware = Literal["legacy", "modern"]


type ListPartes = list[tuple[list[dict[str, str]], list[dict[str, str]]]]
type MethodsSearch = Literal["peticionamento", "consulta"]
type PolosProcessuais = Literal["Passivo", "Ativo"]
type PyNumbers = int | float | complex | datetime | timedelta
type PyStrings = str | bytes
type Dict = dict[str, PyStrings | PyNumbers]
type ListDict = list[Dict]
type StatusBot = Literal["Inicializando", "Em Execução", "Finalizado"]


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
