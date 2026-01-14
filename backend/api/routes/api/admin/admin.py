"""Rotas de API/Socketio para gerenciamento de credenciais dos robôs."""

from __future__ import annotations

from typing import TYPE_CHECKING

from quart import Response, current_app, jsonify, request

from backend.api.decorators import CrossDomain, async_jwt_required
from backend.api.routes._blueprints import admin

from ._credencial import CredencialBot

if TYPE_CHECKING:
    from flask_sqlalchemy import SQLAlchemy


@admin.post("/cadastro_credencial")
@CrossDomain(origin="*", methods=["get", "post", "options"])
@async_jwt_required
def cadatro_credencial() -> Response:  # noqa: D103

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

    response = jsonify(payload)
    response.status_code = status_code
    return response


admin.post("/deletar_credencial")(
    CrossDomain(origin="*", methods=["get", "post", "options"])(
        async_jwt_required(CredencialBot.deletar_credencial),
    ),
)
