"""Gerencie rotas principais e registro de blueprints da aplicação.

Este módulo define rotas básicas e integra blueprints de autenticação e bots.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from flask import (
    Flask,
    Response,
    jsonify,
    make_response,
    redirect,
    request,
    send_from_directory,
    url_for,
)

from api import app
from api.extensions import db
from api.routes import handlers
from api.routes.auth import auth
from api.routes.bots import bots

if TYPE_CHECKING:
    from api.types_app import HealtCheck


__all__ = ["handlers"]


@app.route("/health")
def health_check() -> HealtCheck:
    try:
        # Testa conexão com banco de dados
        db.session.execute(db.text("SELECT 1"))
        db_status = "ok"
        code_err = 200
    except Exception as e:
        app.logger.exception(f"Health check failed: {e}")
        db_status = "erro"
        code_err = 500

    return make_response(
        jsonify({
            "status": "ok" if db_status == "ok" else "erro",
            "database": db_status,
            "timestamp": str(db.func.now()),  # pyright: ignore[reportPossiblyUnboundVariable]
        }),
        code_err,
    )


@app.route("/", methods=["GET"])
def index() -> Response:
    return make_response(redirect(url_for("health_check")))


@app.route("/robots.txt")
def static_from_root() -> Response:
    return send_from_directory(app.static_folder, request.path[1:])  # pyright: ignore[reportArgumentType]


def register_routes(app: Flask) -> None:
    blueprints = [auth, bots]
    for blueprint in blueprints:
        app.register_blueprint(blueprint)


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
