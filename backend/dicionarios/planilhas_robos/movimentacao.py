# ruff: noqa: D100, D101

from __future__ import annotations

from typing import Literal

from ._main import PJe


class PJeMovimentacao(PJe):
    REGIAO: str
    TRAZER_DOCUMENTOS: Literal["sim", "não"]
