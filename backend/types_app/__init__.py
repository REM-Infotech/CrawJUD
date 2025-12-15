"""Defina tipos e aliases para uso em todo o projeto.

Este módulo centraliza definições de tipos e aliases
para padronizar e facilitar o desenvolvimento.
"""

from __future__ import annotations

from datetime import datetime, timedelta
from os import PathLike
from typing import Any, Literal, ParamSpec, TypedDict, TypeVar

from backend.types_app.bot import MessageLog
from backend.types_app.bot.string_types import MessageType

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
type AnyType = Any
type MethodsSearch = Literal["peticionamento", "consulta"]
type PolosProcessuais = Literal["Passivo", "Ativo"]
type PyNumbers = int | float | complex | datetime | timedelta
type PyStrings = str | bytes
type Dict = dict[str, PyStrings | PyNumbers]
type ListDict = list[Dict]
type ListPartes = list[tuple[ListDict], list[ListDict]]
type StatusBot = Literal["Inicializando", "Em Execução", "Finalizado"]
type StrPath = str | PathLike[str]
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


__all__ = ["MessageLog", "MessageType"]
