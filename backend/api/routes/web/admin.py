# ruff: noqa: D101, D100, D107

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, TypedDict
from zoneinfo import ZoneInfo

from flask_jwt_extended import get_current_user
from quart_socketio import Namespace

if TYPE_CHECKING:
    from quart_socketio import SocketIO

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


class AdminNamespace(Namespace):
    def __init__(self, socketio: SocketIO = None) -> None:

        namespace = "/admin"
        super().__init__(namespace, socketio)

    def on_disconnect(self, *args: Any) -> None:

        return ""

    def on_connect(self, *args: Any, **kwargs: Any) -> None:

        return ""

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

    def on_listagem_usuarios(self) -> list[UsuarioItem]:

        user: User = get_current_user()
        now = datetime.now(tz=ZoneInfo("America/Sao_Paulo"))

        return [
            UsuarioItem(
                Id=item.Id,
                nome_Usuario=item.nome_usuario,
                login_usuario=item.login,
                email=item.email,
                ultimo_login=now.strftime("%d/%m/%Y, %H:%M:%S"),
            )
            for item in user.license_.usuarios
        ]
