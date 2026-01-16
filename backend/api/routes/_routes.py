"""Gerencie rotas principais e registro de blueprints da aplicação.

Este módulo define rotas básicas e integra blueprints de autenticação e bots.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from quart import (
    Quart,
    Response,
    jsonify,
    request,
)

from backend.extensions import app, celery

from . import api, status
from ._blueprints import admin, auth, bots, upload
from .web import AdminNamespace, BotNamespace, FileUploadNamespace

if TYPE_CHECKING:
    from quart_socketio import SocketIO


__all__ = ["api", "status"]


async def register_routes(app: Quart) -> None:
    blueprints = [auth, bots, admin, upload]
    for blueprint in blueprints:
        app.register_blueprint(blueprint)

    sio: SocketIO = app.extensions["socketio"]

    async with app.app_context():
        for ns in [AdminNamespace, BotNamespace, FileUploadNamespace]:
            sio.on_namespace(ns(sio))


@app.after_request
def apply_cors(response: Response) -> Response:
    origin = request.headers.get("Origin")
    if origin:
        # Reflete o origin enviado pelo cliente
        response.headers["Access-Control-Allow-Origin"] = origin
        response.headers["Vary"] = "Origin"

        # Permitir credenciais
        response.headers["Access-Control-Allow-Credentials"] = "true"

        # Headers permitidos
        response.headers["Access-Control-Allow-Headers"] = (
            "Content-Type, Authorization, X-Requested-With"
        )

        # Métodos permitidos
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"

    return response


@app.post("/start")
def start_teste() -> None:

    config = request.get_json()["config"]

    _task = celery.tasks["tarefa-prototipo"].apply_async(
        kwargs={
            "config": config,
        },
    )

    return jsonify({"ok": "ok"})
