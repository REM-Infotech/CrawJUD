"""CrawJUD - Sistema de Automação Jurídica."""

import importlib

from celery import Celery
from dynaconf import FlaskDynaconf

from backend import _hook
from backend.task_manager.base import FlaskTask
from backend.task_manager.config import CeleryConfig, config

__all__ = ["_hook"]


celery_app = Celery(__name__, task_cls=FlaskTask)


def make_celery() -> Celery:
    """Create and configure a Celery instance with Quart application context.

    Returns:
        Celery: Configured Celery instance.

    """
    from backend.api import app as flaskapp

    FlaskDynaconf(
        app=flaskapp,
        instance_relative_config=True,
        dynaconf_instance=config,
    )

    celery_app.config_from_object(CeleryConfig(flaskapp.config))

    celery_app.conf.update(
        worker_hijack_root_logger=False,
        worker_redirect_stdouts=False,
    )
    celery_app.set_default()
    flaskapp.extensions["celery"] = celery_app

    importlib.import_module("backend.task_manager.tasks", __package__)

    return celery_app


app = make_celery()
