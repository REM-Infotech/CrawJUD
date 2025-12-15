"""Pacote de útilitários de formatação de strings para o CrawJUD."""

import re
from contextlib import suppress
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from flask import current_app, request
from IP2Location import IP2Location

WORKDIR_PATH = Path.cwd()
T_PATERN = r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:[+-]\d{2}:\d{2}|Z)?$"
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


def get_ip2location_instance() -> IP2Location:
    """Obtenha uma instância do banco de dados IP2Location.

    Returns:
        IP2Location: Instância carregada do banco de dados IP2Location.

    """
    path = WORKDIR_PATH.joinpath("data", "IP2LOCATION-LITE-DB11.BIN")
    return IP2Location(filename=str(path))


def detect_datetime_format(str_dt: str) -> datetime:
    """Detecta o formato da string de data/hora e retorne um objeto datetime.

    Args:
        str_dt (str): String de data/hora a ser analisada.

    Returns:
        datetime: Objeto datetime correspondente à string fornecida.

    Raises:
        ValueError: Quando o formato da string não é reconhecido.

    """

    def raise_value_error() -> None:
        raise ValueError(
            message=f"Formato de data/hora inválido: {str_dt}",
        )

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


def load_timezone() -> str:
    """Obtenha o fuso horário do cliente com base no endereço IP.

    Returns:
        str: Nome do fuso horário no formato 'America/Cidade'.

    """
    ip_user = request.remote_addr
    ip2 = get_ip2location_instance()
    info = ip2.get_all(ip_user)

    info.region = info.region.replace(" ", "_")
    info.city = info.city.replace(" ", "_")

    return f"America/{info.city}"


def update_timezone(dt: datetime | str) -> str:
    """Atualize o horário informado para o fuso horário do cliente.

    Args:
        dt (datetime | str): Data/hora a ser ajustada para o fuso do cliente.

    Returns:
        str: Horário ajustado para o fuso do cliente no formato HH:MM:SS.

    """
    with current_app.app_context():
        client_timezone = request.cookies.get("TimeZone", load_timezone())
        if isinstance(dt, str):
            dt = detect_datetime_format(dt)

        return (
            dt.replace(hour=dt.hour - 1)
            .replace(tzinfo=ZoneInfo(client_timezone))
            .strftime("%H:%M:%S")
        )
