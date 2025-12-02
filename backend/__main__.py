"""Inicie a aplicação Flask e o servidor SocketIO.

Este script é o ponto de entrada principal para a API. Ele cria a aplicação,
carrega as rotas e executa o servidor SocketIO na porta definida.
"""

from __future__ import annotations

import importlib
from os import environ
from threading import Thread
from typing import TYPE_CHECKING

from api import create_app
from celery.apps.worker import Worker
from clear import clear

from backend.task_manager import app as celery_app

if TYPE_CHECKING:
    from flask_socketio import SocketIO

# Porta padrão para execução do servidor Flask
FLASK_PORT: int = 5000

# Crie a aplicação Flask
app = create_app()
# Defina a porta a partir da variável de ambiente ou use o padrão
port: int = int(environ.get("FLASK_PORT", FLASK_PORT)) or FLASK_PORT
# Obtenha a extensão SocketIO da aplicação
io: SocketIO = app.extensions["socketio"]
# Importe rotas para garantir o registro
importlib.import_module("api.routes", __package__)
clear()


worker = Worker(app=celery_app, loglevel="INFO")
task_manager = Thread(target=worker.start, daemon=True)


api = Thread(
    target=io.run,
    args=(app,),
    kwargs={"host": "localhost", "port": port, "allow_unsafe_werkzeug": True},
    daemon=True,
)

api.start()
task_manager.start()
clear()

while True:
    ...
