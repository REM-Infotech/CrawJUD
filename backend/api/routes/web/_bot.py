"""Log bot."""

from __future__ import annotations

from threading import Semaphore
from typing import TYPE_CHECKING, Literal, TypedDict

from flask_jwt_extended import get_current_user
from flask_socketio import join_room

from backend.api.decorators import jwt_sio_required
from backend.api.routes._blueprints import botNS
from backend.utilities import format_time, update_timezone

if TYPE_CHECKING:
    from backend.base import BlueprintNamespace
    from backend.interfaces import Message
    from backend.interfaces.payloads import BotInfo
    from backend.models import User
    from backend.types_app import AnyType, Sistemas

semaphore = Semaphore(1)
semaphore2 = Semaphore(1)

SISTEMAS: set[Sistemas] = {
    "PROJUDI",
    "ELAW",
    "ESAJ",
    "PJE",
    "JUSDS",
    "CSI",
}


def is_sistema(valor: Sistemas) -> bool:
    """Verifique se o valor informado pertence aos sistemas cadastrados.

    Args:
        valor (Sistemas): Valor a ser verificado.

    Returns:
        bool: Indica se o valor está em SISTEMAS.

    """
    return valor in SISTEMAS


class CredenciaisSelect(TypedDict):
    value: int
    text: str


class Execucao(TypedDict):
    Id: 0
    bot: str
    pid: str
    status: str
    data_inicio: str
    data_fim: str


@botNS.on("listagem_execucoes")
@jwt_sio_required
def on_listagem_execucoes(self: BlueprintNamespace) -> list[Execucao]:
    """Lista execuções dos bots do usuário autenticado."""
    # Obtém o usuário autenticado
    user: User = get_current_user()

    # Recupera execuções dos bots do usuário
    execucao = user.execucoes
    if execucao:
        execucao = list(execucao)
        execucao.sort(key=lambda x: x.data_inicio, reverse=True)

    # Define payload padrão caso não haja execuções
    payload: list[Execucao] = []

    if execucao:
        # Retorna lista de execuções se houver
        payload = [
            Execucao(
                Id=item.Id,
                bot=item.bot.display_name,
                pid=item.pid,
                status=item.status,
                data_inicio=format_time(item.data_inicio),
                data_fim=format_time(item.data_fim),
            )
            for item in execucao
        ]

    return payload


@botNS.on("logbot")
@jwt_sio_required
def on_logbot(self: BlueprintNamespace, data: Message) -> None:
    """Log bot."""
    updated = update_timezone(data["time_message"])
    data["time_message"] = f"{updated.strftime('%H:%M:%S')} ({updated.tzname()})"
    # Define diretório temporário para logs
    self.emit(
        "logbot",
        data=data,
        room=data["pid"],
        namespace="/bot",
    )


@botNS.on("listagem")
@jwt_sio_required
def on_listagem(
    self: BlueprintNamespace,
    *args: AnyType,
    **kwargs: AnyType,
) -> list[BotInfo]:
    """Lista todos os bots disponíveis para o usuário autenticado.

    Returns:
        list[BotInfo]: Lista de bots disponíveis para o usuário.

    """
    user: User = get_current_user()

    return {
        "listagem": [
            {
                "Id": bot.Id,
                "display_name": bot.display_name,
                "sistema": bot.sistema,
                "categoria": bot.categoria,
                "configuracao_form": bot.configuracao_form,
                "descricao": bot.descricao,
            }
            for bot in user.license_.bots
        ],
    }


@botNS.on("bot_stop")
@jwt_sio_required
def on_bot_stop(self: BlueprintNamespace, data: dict[str, str]) -> None:
    """Registre parada do bot e salve log."""
    # Emite evento de parada do bot para a sala correspondente
    self.emit("bot_stop", room=data["pid"], namespace="/bot")


@botNS.on("join_room")
@jwt_sio_required
def on_join_room(self: BlueprintNamespace, data: dict[str, str]) -> list[str]:
    """Adicione usuário à sala e retorne logs."""
    # Adiciona o usuário à sala especificada
    join_room(data["room"])


@botNS.on("provide_credentials")
@jwt_sio_required
def on_provide_credentials(
    self: BlueprintNamespace,
    data: dict[Literal["sistema"], Sistemas],
) -> list[CredenciaisSelect]:
    """Lista as credenciais disponíveis para o sistema informado."""
    sistema = data.get("sistema")
    list_credentials = [CredenciaisSelect(value=None, text="Selecione")]

    if not sistema:
        return list_credentials

    if is_sistema(sistema):
        system = sistema.upper()
        user: User = get_current_user()

        lic = user.license_

        list_credentials.extend([
            {"value": credential.Id, "text": credential.nome_credencial}
            for credential in list(
                filter(
                    lambda credential: credential.sistema == system,
                    lic.credenciais,
                ),
            )
        ])

    return list_credentials


@botNS.on("connect")
@jwt_sio_required
def on_connect(self: BlueprintNamespace, *args: AnyType, **kwargs: AnyType) -> None:
    """Log bot."""
    print(args)
    print(kwargs)


@botNS.on("disconnect")
@jwt_sio_required
def on_disconnect(self: BlueprintNamespace, *args: AnyType, **kwargs: AnyType) -> None:
    """Log bot."""
