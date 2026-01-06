from pathlib import Path
from re import Pattern
from typing import Literal

from flask import Response as FlaskResponse

from .payloads import PayloadDownloadExecucao
from .string_types import MessageLog, ProcessoCNJ

type Any = any
type ListPattern = list[Pattern]
type Dict = dict[str, str | Any | None]
type MessageType = Literal["info", "log", "error", "warning", "success"]
type ModeMiddleware = Literal["legacy", "modern"]
type MethodsSearch = Literal["peticionamento", "consulta"]
type PolosProcessuais = Literal["Passivo", "Ativo"]
type StatusBot = Literal["Inicializando", "Em Execução", "Finalizado"]
type StrPath = str | Path
type Sistemas = Literal["PROJUDI", "ESAJ", "ELAW", "JUSDS", "PJE"]
type Contadores = Literal["total", "sucessos", "erros", "restantes"]
type StatusBot = Literal["Inicializando", "Em Execução", "Finalizado"]
type ConfigForm = Literal[
    "file_auth",
    "multiple_files",
    "only_auth",
    "only_file",
    "pje",
    "pje_protocolo",
    "proc_parte",
]
type Methods = Literal[
    "GET",
    "POST",
    "PUT",
    "DELETE",
    "PATCH",
    "OPTIONS",
]


class Response[T](FlaskResponse): ...


__all__ = ["MessageLog", "PayloadDownloadExecucao", "ProcessoCNJ", "Response"]
