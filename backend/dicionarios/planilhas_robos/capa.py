from typing import Literal

from ._main import PJe


class PJeCapa(PJe):
    TRAZER_ASSUNTOS: Literal["sim", "não"]
    TRAZER_PARTES: Literal["sim", "não"]
    TRAZER_AUDIENCIAS: Literal["sim", "não"]
    TRAZER_MOVIMENTACOES: Literal["sim", "não"]
