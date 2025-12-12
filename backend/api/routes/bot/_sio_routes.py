"""Log bot."""

from __future__ import annotations

import json
from contextlib import suppress
from datetime import datetime
from pathlib import Path
from tempfile import gettempdir
from threading import Lock
from typing import TYPE_CHECKING
from zoneinfo import ZoneInfo

from flask import request
from flask_socketio import join_room
from IP2Location import IP2Location

from backend.api.extensions import io

if TYPE_CHECKING:
    from backend.api.interfaces import Message
    from backend.api.types_app import AnyType
import re

lock = Lock()

T_PATERN = (
    r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:[+-]\d{2}:\d{2}|Z)?$"
)
T_PATERN2 = r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d+[+-]\d{2}:\d{2}$"

TIME_PATTERNS = [
    (r"^\d{2}:\d{2}:\d{2}:\d{6}[+-]\d{4}$", "%H:%M:%S:%f%z"),
    (r"^\d{2}:\d{2}:\d{2}[+-]\d{4}$", "%H:%M:%S%z"),
    (r"^\d{2}:\d{2}:\d{2}:\d{6}$", "%H:%M:%S:%f"),
    (r"^\d{2}:\d{2}:\d{2}$", "%H:%M:%S"),
    (r"^\d{4}-\d{2}-\d{2}$", "%Y-%m-%d"),
    (r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$", "%Y-%m-%d %H:%M:%S"),
    (T_PATERN, "%Y-%m-%dT%H:%M:%S"),
    (r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d+$", "%Y-%m-%d %H:%M:%S.%f"),
    (r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}[+-]\d{4}$", "%Y-%m-%d %H:%M:%S%z"),
    (T_PATERN2, "%Y-%m-%dT%H:%M:%S.%f%z"),
]


def load_ip2location_db() -> IP2Location:

    path = Path.cwd().joinpath("data", "IP2LOCATION-LITE-DB11.BIN")
    return IP2Location(filename=str(path))


def loukup_strcurrentformattime(str_dt: str) -> str:
    """Verifica qual o formato da string de data/hora e retorna no formato correto.

    Args:
        str_dt (str): String de data/hora.

    Returns:
        datetime: Objeto datetime correspondente à string fornecida.


    """

    def raise_value_error() -> None:
        raise ValueError(message=f"Formato de data/hora inválido: {str_dt}")

    for pattern, fmt in TIME_PATTERNS:
        if re.match(pattern, str_dt):
            with suppress(ValueError):
                strp_dt = datetime.strptime(str_dt, fmt)  # noqa: DTZ007

                return strp_dt.replace(
                    tzinfo=ZoneInfo("America/Sao_Paulo"),
                    hour=strp_dt.hour - 1,
                )

    raise_value_error()
    return None


def update_timezone(dt: datetime | str) -> str:
    client_timezone = request.cookies.get("TimeZone")

    ip_user = request.remote_addr

    if not client_timezone:
        ip2 = load_ip2location_db()
        info = ip2.get_all(ip_user)

        info.region = info.region.replace(" ", "_")
        info.city = info.city.replace(" ", "_")

        client_timezone = f"America/{info.city}"

    if isinstance(dt, str):
        dt = loukup_strcurrentformattime(dt)

    dt: datetime = dt.replace(hour=dt.hour - 1)
    tz = ZoneInfo(client_timezone)
    dt_aware = dt.replace(tzinfo=tz)
    return dt_aware.strftime("%H:%M:%S")


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


@io.on("logbot", namespace="/bot_logs")
def log_bot(data: Message) -> None:
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
            namespace="/bot_logs",
        )


@io.on("bot_stop", namespace="/bot_logs")
def bot_stop(data: dict[str, str]) -> None:
    """Registre parada do bot e salve log.

    Args:
        data (dict[str, str]): Dados da mensagem do bot.

    """
    # Emite evento de parada do bot para a sala correspondente
    io.emit("bot_stop", room=data["pid"], namespace="/bot_logs")
