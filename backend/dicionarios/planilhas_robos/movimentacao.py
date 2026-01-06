from __future__ import annotations

from typing import Literal

from .main import PJe


class PJeMovimentacao(PJe):
    REGIAO: str
    TRAZER_DOCUMENTOS: Literal["sim", "não"]
