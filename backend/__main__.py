"""Inicie a aplicação Flask e o servidor SocketIO.

Este script é o ponto de entrada principal para a API. Ele cria a aplicação,
carrega as rotas e executa o servidor SocketIO na porta definida.
"""

from __future__ import annotations

from os import environ
from threading import Thread
from typing import TYPE_CHECKING

from celery.apps.worker import Worker

from backend.api import create_app

if TYPE_CHECKING:
    from flask_socketio import SocketIO

FLASK_PORT: int = 5000

app = create_app()


def _start_api() -> None:
    from backend.api import routes as routes

    io: SocketIO = app.extensions["socketio"]
    port: int = int(environ.get("FLASK_PORT", FLASK_PORT)) or FLASK_PORT

    io.run(app, host="localhost", port=port, allow_unsafe_werkzeug=True)


def _start_worker() -> None:
    from backend.task_manager import app as celery_app

    worker = Worker(app=celery_app, loglevel="INFO")
    worker.start()


api_thread = Thread(target=_start_api, daemon=True)
worker_thread = Thread(target=_start_worker, daemon=True)

api_thread.start()
worker_thread.start()

while True:
    ...
