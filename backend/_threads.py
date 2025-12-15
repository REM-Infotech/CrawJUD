from typing import TYPE_CHECKING

from celery.apps.worker import Worker
from clear import clear
from dotenv import dotenv_values

if TYPE_CHECKING:
    from flask_socketio import SocketIO

environ = dotenv_values()
FLASK_PORT: int = 5000
clear()


def _api() -> None:
    from backend.api import create_app
    from backend.api import routes as routes

    flaskapp = create_app()
    io: SocketIO = flaskapp.extensions["socketio"]
    port: int = int(environ.get("FLASK_PORT", FLASK_PORT)) or FLASK_PORT

    io.run(flaskapp, host="localhost", port=port, allow_unsafe_werkzeug=True)


def _celery_worker() -> None:
    from backend.task_manager import app as celery_app

    worker = Worker(app=celery_app, loglevel="INFO")
    worker.start()
