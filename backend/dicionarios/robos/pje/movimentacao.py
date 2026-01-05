from typing import Literal, TypedDict


class PJeMovimentacao(TypedDict):
    NUMERO_PROCESSO: str
    GRAU: str
    REGIAO: str
    TRAZER_MOVIMENTACAO: Literal["sim", "não"]
