"""Módulo de controle de exceptions dos bots."""

from __future__ import annotations

from backend.task_manager.common.exceptions import (
    BaseCrawJUDError as BaseCrawJUDError,
)
from backend.task_manager.common.exceptions import formata_msg as formata_msg

MessageError = "Erro ao executar operaçao: "

__all__ = ["BaseCrawJUDError", "MessageError", "formata_msg"]
