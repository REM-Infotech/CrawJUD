from pathlib import Path
from re import Pattern
from typing import Literal

from cryptography.hazmat.primitives.asymmetric.dh import DHPrivateKey
from cryptography.hazmat.primitives.asymmetric.dsa import DSAPrivateKey
from cryptography.hazmat.primitives.asymmetric.ec import EllipticCurvePrivateKey
from cryptography.hazmat.primitives.asymmetric.ed448 import Ed448PrivateKey
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey
from cryptography.hazmat.primitives.asymmetric.x448 import X448PrivateKey
from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey
from flask import Response as FlaskResponse

from .payloads import PayloadDownloadExecucao
from .string_types import MessageLog, ProcessoCNJ

type TableArgs = dict[Literal["extend_existing"], bool]
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


type PrivateKey = (
    DHPrivateKey
    | Ed25519PrivateKey
    | Ed448PrivateKey
    | RSAPrivateKey
    | DSAPrivateKey
    | EllipticCurvePrivateKey
    | X25519PrivateKey
    | X448PrivateKey
)
type Algoritmos = Literal["SHA256withRSA", "SHA1withRSA", "MD5withRSA"]

__all__ = [
    "Algoritmos",
    "Any",
    "ConfigForm",
    "Contadores",
    "Dict",
    "ListPattern",
    "MessageLog",
    "MessageType",
    "Methods",
    "MethodsSearch",
    "ModeMiddleware",
    "PayloadDownloadExecucao",
    "PolosProcessuais",
    "PrivateKey",
    "ProcessoCNJ",
    "Response",
    "Sistemas",
    "StatusBot",
    "StrPath",
    "TableArgs",
]
