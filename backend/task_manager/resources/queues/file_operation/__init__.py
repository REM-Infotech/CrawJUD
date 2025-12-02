"""Operações de planilhas."""

from backend.task_manager.resources.queues.file_operation.error import SaveError
from backend.task_manager.resources.queues.file_operation.success import SaveSuccess

__all__ = ["SaveError", "SaveSuccess"]
