"""Módulo de tipos do task manager."""

from datetime import datetime, timedelta
from os import PathLike
from typing import Any, Literal, ParamSpec, TypeVar

from backend.task_manager.types_app.bot import MessageLog
from backend.task_manager.types_app.bot.string_types import MessageType

P = ParamSpec("P")
T = TypeVar("T")

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

__all__ = ["MessageLog", "MessageType"]
