from typing import Literal

from ._main import PJe


class PJeMovimentacao(PJe):
    REGIAO: str
    TRAZER_DOCUMENTOS: Literal["sim", "não"]
