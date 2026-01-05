"""CrawJUD - Sistema de Automação Jurídica."""

from __future__ import annotations

from typing import TYPE_CHECKING

from celery import Celery
from celery.signals import after_setup_logger

from backend import _hook
from backend.base import FlaskTask
from backend.config import CeleryConfig, settings
from backend.resources import setup_logger

if TYPE_CHECKING:
    from flask import Flask
__all__ = ["_hook", "settings"]


celery_app = Celery(__name__, task_cls=FlaskTask)
after_setup_logger.connect(setup_logger)


def make_celery(app: Flask) -> Celery:
    """Create and configure a Celery instance with Quart application context.

    Returns:
        Celery: Configured Celery instance.

    """
    from backend.task_manager import tasks as tasks

    celery_app.config_from_object(CeleryConfig(app.config))
    celery_app.set_default()
    app.extensions["celery"] = celery_app

    return celery_app
