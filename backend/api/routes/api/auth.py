"""Módulo de controle das rotas de autenticação da API."""

from __future__ import annotations

import traceback
from contextlib import suppress
from typing import TYPE_CHECKING

from flask_jwt_extended import (
    create_access_token,
    set_access_cookies,
    unset_jwt_cookies,
)
from quart import (
    Response,
    abort,
    current_app,
    jsonify,
    request,
)
from werkzeug.exceptions import HTTPException

from backend.api.routes._blueprints import auth
from backend.models import User

if TYPE_CHECKING:
    from flask_sqlalchemy import SQLAlchemy


@auth.post("/login")
async def login() -> Response:
    """Rota de autenticação da api.

    Returns:
        Response: Response da autenticação

    """
    try:
        db: SQLAlchemy = current_app.extensions["sqlalchemy"]
        data = {}
        with suppress(Exception):
            data = await request.get_json(force=True)  # força o parsing do JSON

        # Verifica se os campos obrigatórios estão presentes
        if not data or not data.get("username") or not data.get("password"):
            payload = jsonify(message="Login e senha são obrigatórios.")
            payload.status_code = 401
            return payload

        user = db.session.query(User).filter_by(login=data["username"]).first()
        authenticated = User.authenticate(
            data["username"],
            data["password"],
        )
        if not authenticated:
            payload = jsonify({"message": "Credenciais inválidas"})
            payload.status_code = 401
            return payload

        if not user:
            payload = jsonify({"message": "Usuário não encontrado."})
            payload.status_code = 401
            return payload

        access_token = create_access_token(identity=str(user.Id))
        response = jsonify(
            message="Login efetuado com sucesso!",
            access_token=access_token,
        )
        response.status_code = 200

        set_access_cookies(
            response=response,
            encoded_access_token=access_token,
        )

    except HTTPException as e:
        response = jsonify({
            "name": e.name,
            "status": e.code,
            "message": e.description,
        })

        response.status_code = e.code

    except Exception as e:  # noqa: BLE001
        _exc = traceback.format_exception(e)
        abort(500)

    return response


@auth.route("/logout", methods=["POST"])
def logout() -> Response:
    """Rota de logout.

    Returns:
        Response: Response do logout.

    """
    response = jsonify(message="Logout efetuado com sucesso!")
    unset_jwt_cookies(response)
    return response
