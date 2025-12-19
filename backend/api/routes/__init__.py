"""Gerencie rotas principais e registro de blueprints da aplicação.

Este módulo define rotas básicas e integra blueprints de autenticação e bots.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from flask import (
    Flask,
    Response,
    request,
)

from backend.api import app
from backend.api.routes import handlers
from backend.api.routes.auth import auth
from backend.api.routes.bot import BotNS, bots
from backend.api.routes.credentials import CredenciaisRobosNS

from . import status

if TYPE_CHECKING:
    from flask_socketio import SocketIO

__all__ = ["handlers", "status"]

values = dict(handlers: Annotated = []
    app: Quart = None
    host: str = "localhost"
    port: int = 5000
    debug: bool = False
    allow_unsafe_werkzeug: bool = False
    use_reloader: bool = False
    extra_files: List[str] = []
    reloader_options: Dict[str, Any] = {}
    server_options: Dict[str, Any] = {}
    launch_mode: str = "uvicorn"
    server: ASyncServerType = None
    namespace_handlers: List[Any] = []
    exception_handlers: Dict[str, Any] = {}
    default_exception_handler: Any = None
    manage_session: bool = True
    log_config: Dict[str, Any] = {}
    log_level: int = 20  # Default to logging.INFO
)

def register_routes(app: Flask) -> None:
    blueprints = [auth, bots]
    for blueprint in blueprints:
        app.register_blueprint(blueprint)

    sio: SocketIO = app.extensions["socketio"]

    with app.app_context():
        sio.on_namespace(BotNS())
        sio.on_namespace(CredenciaisRobosNS())


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
        response.headers["Access-Control-Allow-Methods"] = (
            "GET, POST, PUT, DELETE, OPTIONS"
        )

    return response
