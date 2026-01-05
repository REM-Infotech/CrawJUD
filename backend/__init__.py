"""Inicie a aplicação Flask e o servidor SocketIO.

Este script é o ponto de entrada principal para a API. Ele cria a aplicação,
carrega as rotas e executa o servidor SocketIO na porta definida.
"""

from __future__ import annotations

import logging
from threading import Thread
from time import sleep
from typing import TYPE_CHECKING, NoReturn

from celery.apps.worker import Worker
from clear import clear
from dotenv import dotenv_values
from typer import Typer

from backend.api import create_app

if TYPE_CHECKING:
    from celery import Celery
    from flask import Flask
    from flask_socketio import SocketIO

environ = dotenv_values()
FLASK_PORT: int = 5000
clear()

typerapp = Typer()

app: Flask = create_app()


def _api() -> None:
    from backend.api import routes as routes

    io: SocketIO = app.extensions["socketio"]
    port: int = int(environ.get("FLASK_PORT", FLASK_PORT)) or FLASK_PORT
    io.run(app, host="localhost", port=port, allow_unsafe_werkzeug=True)


def _celery_worker() -> None:
    from backend.task_manager import make_celery

    celery_app: Celery = make_celery(app)

    worker = Worker(
        app=celery_app,
        pool="threads",
        loglevel=logging.INFO,
    )

    worker.start()


@typerapp.command(name="api")
def _thread_api() -> NoReturn:

    api_ = Thread(target=_api, daemon=True)
    api_.start()

    sleep(5)

    while True:
        ...


@typerapp.command(name="celery")
def _thread_celery() -> NoReturn:

    celery_ = Thread(target=_celery_worker, daemon=True)
    celery_.start()

    while True:
        ...


def _start_backend() -> None:

    celery_ = Thread(target=_celery_worker, daemon=True)
    celery_.start()

    api_ = Thread(target=_api, daemon=True)
    api_.start()


__all__ = ["_start_backend", "typerapp"]
