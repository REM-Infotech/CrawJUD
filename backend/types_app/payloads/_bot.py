from __future__ import annotations

from typing import Literal, TypedDict

type SystemBots = Literal["PROJUDI", "ESAJ", "ELAW", "JUSDS", "PJE"]
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


class File(TypedDict):
    name: str
    # Adicione outros campos relevantes conforme necessário


class CertificadoFileType(File):
    pass  # O nome deve terminar com '.pfx'


class KbdxFileType(File):
    pass  # O nome deve terminar com '.kdbx'


type CertificadoFile = CertificadoFileType | None
type KbdxFile = KbdxFileType | None
