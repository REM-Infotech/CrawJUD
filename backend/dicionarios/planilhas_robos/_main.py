from __future__ import annotations

from typing import Literal, TypedDict


class BotData(TypedDict):
    NUMERO_PROCESSO: str
    GRAU: str


class PJe(BotData):
    REGIAO: Literal["1"]
