"""Operações de planilhas."""

from backend.resources.queues.file_operation.error import SaveError
from backend.resources.queues.file_operation.success import (
    SaveSuccess,
)

__all__ = ["SaveError", "SaveSuccess"]
