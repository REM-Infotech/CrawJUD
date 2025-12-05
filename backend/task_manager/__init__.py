"""CrawJUD - Sistema de Automação Jurídica."""

import importlib
import logging

from celery import Celery, signals
from dynaconf import FlaskDynaconf

from backend import _hook
from backend.config._log._handlers import RichQueueHandler
from backend.task_manager.base import FlaskTask
from backend.task_manager.config import CeleryConfig, config
from backend.task_manager.extensions import flaskapp

__all__ = ["_hook"]


@signals.setup_logging.connect
def on_celery_setup_logging(**kwargs) -> list[logging.Handler]:

    logger = logging.getLogger("backend.task_manager")
    logger.addHandler(RichQueueHandler(target="backend.task_manager"))

    return [logger.handlers[0]]


celery_app = Celery(flaskapp.name, task_cls=FlaskTask)


def make_celery() -> Celery:
    """Create and configure a Celery instance with Quart application context.

    Returns:
        Celery: Configured Celery instance.

    """
    FlaskDynaconf(
        app=flaskapp,
        instance_relative_config=True,
        extensions_list="EXTENSIONS",
        dynaconf_instance=config,
    )

    celery_app.config_from_object(CeleryConfig(flaskapp.config))
    celery_app.set_default()
    flaskapp.extensions["celery"] = celery_app

    importlib.import_module("backend.task_manager.tasks", __package__)

    return celery_app


app = make_celery()
