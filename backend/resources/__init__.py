"""Pacote público para recursos do sistema.

Contém arquivos e utilitários de recursos compartilhados.
"""

import re
from logging import FileHandler, Formatter, Logger, StreamHandler
from pathlib import Path

from backend.task_manager.constants import MAIOR_60_ANOS, VER_RECURSO

from .auth.pje import AutenticadorPJe
from .formatadores import formata_string
from .iterators.pje import RegioesIterator

__all__ = [
    "AutenticadorPJe",
    "RegioesIterator",
    "formata_string",
]

type Any = any


def camel_to_snake(name: str) -> str:
    """Converta string CamelCase para snake_case.

    Args:
        name (str): String no formato CamelCase.

    Returns:
        str: String convertida para snake_case.

    """
    # Adiciona underscore antes de letras maiúsculas precedidas de minúsculas
    snake_case_step1 = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", name)
    # Adiciona underscore antes de letras maiúsculas precedidas de números ou minúsculas
    return re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", snake_case_step1).lower()


def value_check(label: str, valor: str) -> bool:
    """Verifique se valor não está em constantes proibidas.

    Args:
        label (str): Rótulo do campo.
        valor (str): Valor a ser verificado.

    Returns:
        bool: True se valor for permitido, senão False.

    """
    # Verifica se o valor não contém ":" e não está nas constantes
    if label and valor and ":" not in valor:
        return valor not in {MAIOR_60_ANOS, VER_RECURSO}

    return False


def setup_logger(
    *args: Any,
    logger: Logger,
    **kwargs: Any,
) -> None:

    _arg = args
    _kwarg = kwargs

    format_ = str(kwargs.get("format"))

    handlers = logger.handlers

    if not format_ and handlers:
        format_ = logger.handlers[0].formatter._fmt  # noqa: SLF001

    name: str = str(kwargs.get("name", "crawjud.log"))

    path_log = Path.cwd().joinpath("logs", name)
    if not path_log.parent.exists():
        path_log.parent.mkdir(exist_ok=True)
        path_log.touch()

    logger.handlers.clear()

    file_handler = FileHandler(path_log)
    file_handler.level = logger.level
    file_handler.formatter = Formatter(format_)

    stream_handler = StreamHandler()
    stream_handler.level = file_handler.level

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger
