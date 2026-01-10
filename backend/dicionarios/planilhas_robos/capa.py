from __future__ import annotations

from typing import Literal

from .main import BotData, PJe


class PJeCapa(PJe):
    TRAZER_ASSUNTOS: Literal["sim", "não"]
    TRAZER_PARTES: Literal["sim", "não"]
    TRAZER_AUDIENCIAS: Literal["sim", "não"]
    TRAZER_MOVIMENTACOES: Literal["sim", "não"]


class ProjudiCapa(BotData):
    TRAZER_COPIA: str
    TRAZER_MOVIMENTACOES: str


class EsajCapa(BotData): ...
