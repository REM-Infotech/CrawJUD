from __future__ import annotations

import asyncio
import logging
from pathlib import Path
from threading import Thread
from typing import TYPE_CHECKING, NoReturn

from celery.apps.worker import Worker
from clear import clear
from dotenv import dotenv_values
from typer import Typer

if TYPE_CHECKING:
    from quart_socketio import SocketIO

environ = dotenv_values()
FLASK_PORT: int = 5000
clear()

typerapp = Typer()

ACCESS_FMT = '%(levelprefix)s %(client_addr)s - "%(request_line)s" %(status_code)s'


def _api() -> None:
    from backend.api import routes as routes

    from .extensions import create_app, make_celery

    log_level = logging.DEBUG
    name = "crawjud-api.log"
    path_log = Path.cwd().joinpath("logs", name)
    if not path_log.parent.exists():
        path_log.parent.mkdir(exist_ok=True)
        path_log.touch()

    log_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "()": "uvicorn.logging.DefaultFormatter",
                "fmt": "%(levelprefix)s %(asctime)s %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
            "access": {
                "()": "uvicorn.logging.AccessFormatter",
                "fmt": ACCESS_FMT,
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
        },
        "handlers": {
            "default": {
                "formatter": "default",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
            },
            "access": {
                "formatter": "access",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
            },
            "file_log": {
                "formatter": "default",
                "class": "logging.FileHandler",
                "filename": str(path_log),
            },
        },
        "loggers": {
            "uvicorn": {"handlers": ["default"], "level": log_level},
            "uvicorn.error": {
                "handlers": ["default", "file_log"],
                "level": log_level,
                "propagate": False,
            },
            "uvicorn.access": {
                "handlers": ["access", "file_log"],
                "level": log_level,
                "propagate": False,
            },
            "uvicorn.asgi": {
                "handlers": ["default", "file_log"],
                "level": log_level,
                "propagate": False,
            },
            "uvicorn.lifespan": {
                "handlers": ["default", "file_log"],
                "level": log_level,
                "propagate": False,
            },
        },
    }
    with asyncio.Runner() as runner:
        app = runner.run(create_app())
        _celery = make_celery(app)

        io: SocketIO = app.extensions["socketio"]
        port: int = int(environ.get("FLASK_PORT", FLASK_PORT)) or FLASK_PORT
        io.run(app, host="localhost", port=port, log_config=log_config)


@typerapp.command(name="api")
def thread_api() -> NoReturn:

    api_ = Thread(target=_api, daemon=True)
    api_.start()
    while True:
        ...


@typerapp.command(name="celery")
def thread_celery() -> NoReturn:
    from .extensions import create_app, make_celery

    with asyncio.Runner() as runner:
        app = runner.run(create_app())
        celery = make_celery(app)
        worker = Worker(
            app=celery,
            pool="threads",
            loglevel=logging.DEBUG,
            task_events=True,
        )

        worker.start()


__all__ = ["typerapp"]
