from __future__ import annotations

from typing import Literal

from .main import BotData, PJe


class PJeMovimentacao(PJe):
    REGIAO: str
    TRAZER_DOCUMENTOS: Literal["sim", "não"]


class ProdudiMovimentacao(BotData):
    PALAVRAS_CHAVE: str
    TRAZER_ARQUIVO_MOVIMENTACAO: Literal["sim", "não"]
