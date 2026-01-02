# ruff: noqa: D100, D101
from __future__ import annotations

from ._main import BotData


class Provisionamento(BotData):
    PROVISAO: str
    VALOR_ATUALIZACAO: str


class JusdsProvisionamento(BotData):
    MOMENTO_PROCESSUAL: str
    ORIGEM_RISCO: str
    CRITERIO_DETERMINANTE: str
    STATUS_EVENTO: str


class ElawProvisionamento(BotData): ...
