"""Log bot."""

from __future__ import annotations

import json
from pathlib import Path
from tempfile import gettempdir
from threading import Lock
from typing import TYPE_CHECKING

from flask_socketio import join_room

from backend.api.extensions import io

from . import filehandler

if TYPE_CHECKING:
    from backend.api.interfaces import Message
    from backend.api.types_app import AnyType

lock = Lock()

__all__ = ["filehandler"]


@io.on("connect", namespace="/")
def connected(*args: AnyType, **kwargs: AnyType) -> None:
    """Log bot."""


@io.on("join_room", namespace="/bot_logs")
def join_room_bot(data: dict[str, str]) -> list[str]:
    """Adicione usuário à sala e retorne logs.

    Args:
        data (dict[str, str]): Dados contendo a sala.

    Returns:
        list[str]: Lista de mensagens do log.

    """
    # Adiciona o usuário à sala especificada
    join_room(data["room"])

    # Inicializa a lista de mensagens
    messages: list[str] = []
    temp_dir = Path(gettempdir()).joinpath("crawjud", "logs")
    log_file = temp_dir.joinpath(f"{data['room']}.log")
    _str_dir = str(log_file)
    # Se o diretório e o arquivo de log existem, carrega as mensagens
    if temp_dir.exists() and log_file.exists():
        text_file = log_file.read_text(encoding="utf-8").replace("null", '""')

        messages.extend(json.loads(text_file))
    return messages


@io.on("logbot", namespace="/bot_logs")
def log_bot(data: Message) -> None:
    """Log bot."""
    io.emit(
        "logbot",
        data=data,
        room=data["pid"],
        namespace="/bot_logs",
    )

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


@io.on("bot_stop", namespace="/bot_logs")
def bot_stop(data: dict[str, str]) -> None:
    """Registre parada do bot e salve log.

    Args:
        data (dict[str, str]): Dados da mensagem do bot.

    """
    # Emite evento de parada do bot para a sala correspondente
    io.emit("bot_stop", room=data["pid"], namespace="/bot_logs")
