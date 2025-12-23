"""Log bot."""

from __future__ import annotations

from datetime import datetime
from threading import Lock
from typing import TYPE_CHECKING, Literal, TypedDict
from zoneinfo import ZoneInfo

from flask_jwt_extended import get_current_user
from flask_socketio import Namespace, join_room

from backend.api.decorators import jwt_sio_required
from backend.api.extensions import io
from backend.utilities import format_time, load_timezone, update_timezone

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


class Execucao(TypedDict):
    Id: 0
    bot: str
    pid: str
    status: str
    data_inicio: str
    data_fim: str


class BotNS(Namespace):
    def __init__(self) -> None:
        super().__init__(namespace="/bot")

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
                    pid=item.pid,
                    status=item.status,
                    data_inicio=format_time(item.data_inicio),
                    data_fim=format_time(item.data_fim),
                )
                for item in execucao
            ]

        return payload

    @jwt_sio_required
    def on_logbot(self, data: Message) -> None:
        """Log bot."""
        updated = update_timezone(data["time_message"])
        data["time_message"] = f"{updated.strftime('%H:%M:%S')} ({updated.tzname()})"
        # Define diretório temporário para logs
        # temp_dir: Path = Path(gettempdir()).joinpath("crawjud", "logs") noqa: ERA001  # noqa: E501
        # log_file: Path = temp_dir.joinpath(f"{data['pid']}.log") noqa: ERA001  # noqa: E501
        # # Cria diretório e arquivo de log se não existirem
        # if not temp_dir.exists():
        #     temp_dir.mkdir(parents=True, exist_ok=True) noqa: ERA001

        # if not log_file.exists():
        #     log_file.write_text(json.dumps([]), encoding="utf-8") noqa: ERA001  # noqa: E501

        # # Lê mensagens existentes, adiciona nova e salva novamente
        # read_file: str = log_file.read_text(encoding="utf-8") noqa: ERA001
        # list_messages: list[Message] = json.loads(read_file) noqa: ERA001
        # list_messages.append(data) noqa: ERA001
        # log_file.write_text(json.dumps(list_messages), encoding="utf-8") noqa: ERA001  # noqa: E501

        io.emit(
            "logbot",
            data=data,
            room=data["pid"],
            namespace="/bot",
        )

    @jwt_sio_required
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

    @jwt_sio_required
    def on_bot_stop(self, data: dict[str, str]) -> None:
        """Registre parada do bot e salve log.

        Args:
            data (dict[str, str]): Dados da mensagem do bot.

        """
        # Emite evento de parada do bot para a sala correspondente
        io.emit("bot_stop", room=data["pid"], namespace="/bot")

    @jwt_sio_required
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
        # temp_dir = Path(gettempdir()).joinpath("crawjud", "logs") noqa: ERA001  # noqa: E501
        # log_file = temp_dir.joinpath(f"{data['room']}.log") noqa: ERA001
        # _str_dir = str(log_file) noqa: ERA001
        now = datetime.now(ZoneInfo(load_timezone()))

        def map_messages(msg: Message) -> Message:
            updt = update_timezone(msg["time_message"])
            updated = updt.replace(
                day=now.day,
                month=now.month,
                year=now.year,
            )
            msg["time_message"] = updated.strftime("%H:%M:%S")
            return msg

        # # Se o diretório e o arquivo de log existem, carrega as mensagens
        # if temp_dir.exists() and log_file.exists():
        #     text_file = log_file.read_text(encoding="utf-8").replace("null", '""') noqa: ERA001  # noqa: E501

        #     with suppress(json.JSONDecodeError):
        #         messages.extend(json.loads(text_file)) noqa: ERA001

        return [map_messages(msg) for msg in messages]

    @jwt_sio_required
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

    @jwt_sio_required
    def on_connect(self, *args: AnyType, **kwargs: AnyType) -> None:
        """Log bot."""

    @jwt_sio_required
    def on_disconnect(self, *args: AnyType, **kwargs: AnyType) -> None:
        """Log bot."""
