"""Pacote público para recursos do sistema.

Contém arquivos e utilitários de recursos compartilhados.
"""

from __future__ import annotations

from logging import FileHandler, Formatter, Logger, StreamHandler  # noqa: F401
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typings import Any


def setup_logger(  # noqa: D103
    *args: Any,
    logger: Logger,
    **kwargs: Any,
) -> None:

    format_ = str(kwargs.get("format"))

    handlers = logger.handlers

    if not format_ and handlers:
        format_ = logger.handlers[0].formatter._fmt  # noqa: SLF001

    name: str = str(kwargs.get("name", "crawjud.log"))
    if kwargs.get("signal"):
        name = "crawjud-celery.log"

    path_log = Path.cwd().joinpath("logs", name)
    if not path_log.parent.exists():
        path_log.parent.mkdir(exist_ok=True)
        path_log.touch()

    logger.handlers.clear()

    file_handler = FileHandler(path_log)
    file_handler.level = logger.level
    file_handler.formatter = Formatter(format_)

    logger.addHandler(file_handler)

    return logger
