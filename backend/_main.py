from __future__ import annotations

import logging
from pathlib import Path
from threading import Thread
from time import sleep
from typing import TYPE_CHECKING, NoReturn

from celery.apps.worker import Worker
from clear import clear
from dotenv import dotenv_values
from typer import Typer

from .extensions import create_app, make_celery

if TYPE_CHECKING:
    from celery import Celery
    from flask import Flask
    from flask_socketio import SocketIO

environ = dotenv_values()
FLASK_PORT: int = 5000
clear()

typerapp = Typer()

app: Flask = create_app()


def _api(app: Flask) -> None:
    from backend.api import routes as routes

    io: SocketIO = app.extensions["socketio"]
    port: int = int(environ.get("FLASK_PORT", FLASK_PORT)) or FLASK_PORT
    io.run(app, host="localhost", port=port, allow_unsafe_werkzeug=True)


def _celery_worker(celery: Celery) -> None:

    worker = Worker(
        app=celery,
        pool="threads",
        loglevel=logging.INFO,
    )

    worker.start()


@typerapp.command(name="api")
def _thread_api() -> NoReturn:

    app = create_app()
    make_celery(app)
    api_ = Thread(target=_api, daemon=True, kwargs={"app": app})
    api_.start()

    sleep(5)

    logger = logging.getLogger("werkzeug")

    name = "crawjud-api.log"
    path_log = Path.cwd().joinpath("logs", name)
    if not path_log.parent.exists():
        path_log.parent.mkdir(exist_ok=True)
        path_log.touch()

    file_handler = logging.FileHandler(path_log)
    file_handler.level = logger.level

    logger.addHandler(file_handler)

    while True:
        ...


@typerapp.command(name="celery")
def _thread_celery() -> NoReturn:

    app = create_app()
    celery: Celery = make_celery(app)
    celery_ = Thread(target=_celery_worker, daemon=True, kwargs={"celery": celery})
    celery_.start()

    while True:
        ...


def _start_backend() -> None:

    app = create_app()
    celery = make_celery(app)

    celery_ = Thread(target=_celery_worker, daemon=True, kwargs={"celery": celery})
    celery_.start()

    api_ = Thread(target=_api, daemon=True, kwargs={"app": app})
    api_.start()


__all__ = ["_start_backend", "typerapp"]
