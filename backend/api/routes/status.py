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
from flask_jwt_extended import jwt_required

from backend.api import app
from backend.api.routes import handlers
from backend.extensions import db

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
    except Exception as e:  # noqa: BLE001
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


@app.route("/sessao-valida", methods=["GET"])
@jwt_required()
def sessao_valida() -> Response:
    """Verifica se a sessão JWT é válida.

    Retorna um status 200 se a sessão for válida, caso contrário,
    retorna um erro 401.

    Returns:
        Response: Resposta HTTP indicando o status da sessão.

    """
    return make_response(jsonify({"msg": "Sessão válida"}), 200)
