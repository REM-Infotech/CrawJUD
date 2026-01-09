"""Registre tasks Celery do sistema CrawJUD.

Este módulo centraliza o registro das principais tasks do projeto.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from backend._makers import celery_app

from .bots import EsajCapaTask, PJeCapaTask, ProjudiCapaTask
from .mail import MailTasks

if TYPE_CHECKING:
    from backend.base import CeleryTask

tasks: list[CeleryTask] = [MailTasks, PJeCapaTask, ProjudiCapaTask, EsajCapaTask]


def register_tasks() -> None:  # noqa: D103

    for task in tasks:
        celery_app.register_task(task())


__all__ = ["register_tasks"]
