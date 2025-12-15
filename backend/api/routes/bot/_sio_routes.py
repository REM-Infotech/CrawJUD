"""Log bot."""

from __future__ import annotations

import json
from contextlib import suppress
from datetime import datetime
from pathlib import Path
from tempfile import gettempdir
from threading import Lock
from typing import TYPE_CHECKING, Literal, TypedDict
from uuid import uuid4

from flask_jwt_extended import get_current_user, jwt_required
from flask_socketio import Namespace, join_room

from backend.api.extensions import io
from backend.utilities import update_timezone

if TYPE_CHECKING:
    from backend.api.models import User
    from backend.interfaces import Message
    from backend.interfaces.payloads import BotInfo
    from backend.types_app import AnyType, Sistemas

lock = Lock()


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


class BotNS(Namespace):
    def __init__(self) -> None:
        super().__init__(namespace="/bot")

    @jwt_required()
    def on_logbot(self, data: Message) -> None:
        """Log bot."""
        with lock:
            strp_dt = datetime.strptime(data.get("time_message"), "%H:%M:%S:%z")
            data["time_message"] = update_timezone(strp_dt)
            # Define diretório temporário para logs
            temp_dir: Path = Path(gettempdir()).joinpath("crawjud", "logs")
            log_file: Path = temp_dir.joinpath(f"{data['pid']}.log")
            # Cria diretório e arquivo de log se não existirem
            if not temp_dir.exists():
                temp_dir.mkdir(parents=True, exist_ok=True)

            if not log_file.exists():
                log_file.write_text(json.dumps([]), encoding="utf-8")

            # Lê mensagens existentes, adiciona nova e salva novamente
            read_file: str = log_file.read_text(encoding="utf-8")
            list_messages: list[Message] = json.loads(read_file)
            list_messages.append(data)
            log_file.write_text(json.dumps(list_messages), encoding="utf-8")

            io.emit(
                "logbot",
                data=data,
                room=data["pid"],
                namespace="/bot",
            )

    @jwt_required()
    def on_listagem(self, *args: AnyType, **kwargs: AnyType) -> list[BotInfo]:
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

    @jwt_required()
    def on_bot_stop(self, data: dict[str, str]) -> None:
        """Registre parada do bot e salve log.

        Args:
            data (dict[str, str]): Dados da mensagem do bot.

        """
        # Emite evento de parada do bot para a sala correspondente
        io.emit("bot_stop", room=data["pid"], namespace="/bot")

    @jwt_required()
    def on_join_room(self, data: dict[str, str]) -> list[str]:
        """Adicione usuário à sala e retorne logs.

        Args:
            data (dict[str, str]): Dados contendo a sala.

        Returns:
            list[str]: Lista de mensagens do log.

        """
        # Adiciona o usuário à sala especificada
        join_room(data["room"])

        # Inicializa a lista de mensagens
        messages: list[Message] = []
        temp_dir = Path(gettempdir()).joinpath("crawjud", "logs")
        log_file = temp_dir.joinpath(f"{data['room']}.log")
        _str_dir = str(log_file)

        def map_messages(msg: Message) -> Message:
            msg["time_message"] = update_timezone(msg["time_message"])
            return msg

        # Se o diretório e o arquivo de log existem, carrega as mensagens
        if temp_dir.exists() and log_file.exists():
            text_file = log_file.read_text(encoding="utf-8").replace("null", '""')

            with suppress(json.JSONDecodeError):
                messages.extend(json.loads(text_file))

        return [map_messages(msg) for msg in messages]

    @jwt_required()
    def on_provide_credentials(
        self,
        data: dict[Literal["sistema"], Sistemas],
    ) -> list[CredenciaisSelect]:
        """Lista as credenciais disponíveis para o sistema informado.

        Args:
            data: `dict[Literal["sistema"], Sistemas]`

        Returns:
            Response: Resposta HTTP com as credenciais filtradas.

        """
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

    @jwt_required()
    def on_connected(self, *args: AnyType, **kwargs: AnyType) -> None:
        """Log bot."""
        self.seed = str(uuid4())
