"""Inicie a aplicação Flask e o servidor SocketIO.

Este script é o ponto de entrada principal para a API. Ele cria a aplicação,
carrega as rotas e executa o servidor SocketIO na porta definida.
"""

from __future__ import annotations

import builtins
import inspect
import logging
from contextlib import contextmanager
from os import environ
from threading import Thread
from typing import TYPE_CHECKING

from backend.config._log._layout_console import run_console

if TYPE_CHECKING:
    from collections.abc import Generator


@contextmanager
def _custom_print() -> Generator[None]:

    original_print = builtins.print

    def rich_print(*args, **kwargs) -> None:

        frame = inspect.currentframe()
        modulo = inspect.getmodule(frame.f_back)
        message = " ".join(str(arg) for arg in args)
        target = "backend.api"
        if "celery" in modulo.__name__ or "kombu" in modulo.__name__:
            target = "backend.task_manager"

        from backend.config._log._layout_console import log

        log(message, target)

    builtins.print = rich_print
    yield
    builtins.print = original_print


with _custom_print():
    from celery.apps.worker import Worker

    from backend.api import create_app
    from backend.config._log._handlers import RichQueueHandler
    from backend.task_manager import app as celery_app

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

        worker = Worker(app=celery_app, loglevel="INFO")
        worker.start()

    api_thread = Thread(target=_start_api, daemon=True)
    worker_thread = Thread(target=_start_worker, daemon=True)

    api_thread.start()
    worker_thread.start()

    response_logger = logging.getLogger("werkzeug")
    response_logger.handlers.clear()
    response_logger.addHandler(RichQueueHandler("backend.api"))

    run_console()
