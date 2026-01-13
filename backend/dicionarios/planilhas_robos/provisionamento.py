from __future__ import annotations

from typing import Literal

from .main import BotData


class Provisionamento(BotData):
    PROVISAO: str
    VALOR_ATUALIZACAO: str


class JusdsProvisionamento(BotData):
    PARTE: str
    NIVEL: Literal["ALTO", "MEDIO", "BAIXO"]
    OBJETO_RISCO: str
    OBJETO_PORCENTAGEM: str
    MOMENTO_PROCESSUAL: str
    ORIGEM_RISCO: str
    CRITERIO_DETERMINANTE: str
    VALOR_RISCO: str
    VALOR_PAGO: str
    DATA_PAGAMENTO: str
    HONORARIOS: str
    STATUS_EVENTO: str


class ElawProvisionamento(BotData): ...
