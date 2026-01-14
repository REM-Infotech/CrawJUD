from __future__ import annotations

import asyncio
import logging
from pathlib import Path
from threading import Thread
from time import sleep
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


def _api() -> None:
    from backend.api import routes as routes

    from .extensions import create_app, make_celery

    with asyncio.Runner() as runner:
        app = runner.run(create_app())
        _celery = make_celery(app)

        io: SocketIO = app.extensions["socketio"]
        port: int = int(environ.get("FLASK_PORT", FLASK_PORT)) or FLASK_PORT
        io.run(app, host="localhost", port=port)


@typerapp.command(name="api")
def thread_api() -> NoReturn:

    api_ = Thread(target=_api, daemon=True)
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
