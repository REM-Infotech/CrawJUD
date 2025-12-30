from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, TypedDict
from zoneinfo import ZoneInfo

from flask_jwt_extended import get_current_user, jwt_required

from backend.api.routes._blueprints import adminNS

if TYPE_CHECKING:
    from backend.api.base import BlueprintNamespace
    from backend.models import User

type Any = any


class CredencialItem(TypedDict):
    Id: int
    nome_credencial: str
    tipo_autenticacao: str


class UsuarioItem(TypedDict):
    Id: int
    nome_Usuario: str
    login_usuario: str
    email: str
    ultimo_login: str


@adminNS.on("disconnect")
@jwt_required()
def disconnect(self: BlueprintNamespace, args: Any) -> None:

    return ""


@adminNS.on("connect")
@jwt_required()
def connect(self: BlueprintNamespace, *args: Any, **kwargs: Any) -> None:

    return ""


@adminNS.on("listagem_credenciais")
@jwt_required()
def listagem_credenciais(self: BlueprintNamespace) -> list[CredencialItem]:

    user: User = get_current_user()

    return [
        {
            "Id": item.Id,
            "nome_credencial": item.nome_credencial,
            "tipo_autenticacao": item.login_metodo,
        }
        for item in user.license_.credenciais
    ]


@adminNS.on("listagem_usuarios")
@jwt_required()
def listagem_usuarios(self: BlueprintNamespace) -> list[UsuarioItem]:

    user: User = get_current_user()

    return [
        UsuarioItem(
            Id=item.Id,
            nome_Usuario=item.nome_usuario,
            login_usuario=item.login,
            email=item.email,
            ultimo_login=datetime.now(tz=ZoneInfo("America/Sao_Paulo")),
        )
        for item in user.license_.usuarios
    ]
