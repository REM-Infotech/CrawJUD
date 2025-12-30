"""Rotas de API/Socketio para gerenciamento de credenciais dos robôs."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flask import Blueprint, Response, current_app, jsonify, make_response, request
from flask_jwt_extended import jwt_required

from backend.api.decorators import CrossDomain

from ._credencial import CredencialBot

if TYPE_CHECKING:
    from flask_sqlalchemy import SQLAlchemy


admin = Blueprint("admin", __name__, url_prefix="/admin")


@admin.post("/cadastro_credencial")
@CrossDomain(origin="*", methods=["get", "post", "options"])
@jwt_required()
def cadatro_credencial() -> Response:

    form_ = request.form
    _files = request.files

    payload = {
        "mensagem": "Erro ao salvar credencial",
    }

    status_code = 500

    if form_:
        _db: SQLAlchemy = current_app.extensions["sqlalchemy"]
        CredencialBot(app=current_app, **form_).cadastro()

        payload = {
            "mensagem": "Credencial salva com sucesso!",
        }

        status_code = 200
    return make_response(jsonify(payload), status_code)


admin.post("/deletar_credencial")(
    CrossDomain(origin="*", methods=["get", "post", "options"])(
        jwt_required()(CredencialBot.deletar_credencial),
    ),
)
