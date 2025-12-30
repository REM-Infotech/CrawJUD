from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, TypedDict
from zoneinfo import ZoneInfo

from flask_jwt_extended import get_current_user, jwt_required
from flask_socketio import Namespace

if TYPE_CHECKING:
    from backend.models import User


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


class NamespaceAdminCrawJUD(Namespace):
    def __init__(self) -> None:
        self._namespace = "/admin"
        super().__init__(self._namespace)

    @jwt_required()
    def on_disconnect(self) -> None:

        return ""

    @jwt_required()
    def on_connect(self) -> None:

        return ""

    @jwt_required()
    def on_listagem_credenciais(self) -> list[CredencialItem]:

        user: User = get_current_user()

        return [
            {
                "Id": item.Id,
                "nome_credencial": item.nome_credencial,
                "tipo_autenticacao": item.login_metodo,
            }
            for item in user.license_.credenciais
        ]

    @jwt_required()
    def on_listagem_usuarios(self) -> list[UsuarioItem]:

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
