"""Registre tasks Celery do sistema CrawJUD.

Este módulo centraliza o registro das principais tasks do projeto.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from backend.extensions import celery

from .bots import (
    EsajCapaTask,
    EsajMovimentacaoTask,
    JusdsProvisionamentoTask,
    PJeCapaTask,
    PJeMovimentacaoTask,
    ProjudiCapaTask,
    ProjudiIntimacoesTask,
    ProjudiMovimentacaoTask,
)
from .mail import MailTasks

if TYPE_CHECKING:
    from backend.base import CeleryTask

tasks: list[CeleryTask] = [
    MailTasks,
    PJeCapaTask,
    ProjudiCapaTask,
    EsajCapaTask,
    ProjudiIntimacoesTask,
    ProjudiMovimentacaoTask,
    EsajMovimentacaoTask,
    PJeMovimentacaoTask,
    JusdsProvisionamentoTask,
]


def register_tasks() -> None:  # noqa: D103

    for task in tasks:
        celery.register_task(task())


__all__ = ["register_tasks"]
