"""Log bot."""

from __future__ import annotations

from typing import TYPE_CHECKING, Literal, TypedDict

from flask_jwt_extended import get_current_user
from quart_socketio import Namespace, SocketIO, join_room

from backend.api.decorators import jwt_sio_required

if TYPE_CHECKING:
    from backend.dicionarios import BotInfo, Message
    from backend.models import User
    from typings import Any, Sistemas


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
    id_execucao: str
    status: str
    data_inicio: str
    data_fim: str


class BotNamespace(Namespace):
    def __init__(self, socketio: SocketIO = None) -> None:

        namespace = "/bot"
        super().__init__(namespace, socketio)

    @jwt_sio_required
    def on_listagem_execucoes(self) -> list[Execucao]:
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
                    id_execucao=item.id_execucao,
                    status=item.status,
                    data_inicio=item.data_inicio.strftime("%d/%m/%Y, %H:%M:%S"),
                    data_fim=item.data_fim.strftime("%d/%m/%Y, %H:%M:%S")
                    if item.data_fim
                    else "",
                )
                for item in execucao
            ]

        return payload

    def on_logbot(self, data: Message) -> None:
        """Log bot."""
        self.emit(
            "logbot",
            data=data,
            room=data["id_execucao"],
            namespace="/bot",
        )

    @jwt_sio_required
    def on_listagem(
        self,
        *args: Any,
        **kwargs: Any,
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

    @jwt_sio_required
    def on_bot_stop(self, data: dict[str, str]) -> None:
        """Registre parada do bot e salve log."""
        # Emite evento de parada do bot para a sala correspondente
        self.emit("bot_stop", room=data["id_execucao"], namespace="/bot")

    def on_join_room(
        self,
        data: dict[str, str],
    ) -> list[str]:
        """Adicione usuário à sala e retorne logs."""
        # Adiciona o usuário à sala especificada
        join_room(data["room"])

    @jwt_sio_required
    def on_provide_credentials(
        self,
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

    def on_connect(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Log bot."""

    def on_disconnect(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Log bot."""
