"""Rotas de status da API."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flask import (
    Response,
    jsonify,
    make_response,
    redirect,
    request,
    send_from_directory,
    url_for,
)

from backend.api import app
from backend.api.extensions import db
from backend.api.routes import handlers

if TYPE_CHECKING:
    from backend.types_app import HealtCheck


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
            "timestamp": str(db.func.now()),
        }),
        code_err,
    )


@app.route("/", methods=["GET"])
def index() -> Response:
    return make_response(redirect(url_for("health_check")))


@app.route("/robots.txt")
def static_from_root() -> Response:
    return send_from_directory(app.static_folder, request.path[1:])
