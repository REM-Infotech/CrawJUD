from ._main import BotData


class Movimentacao(BotData):
    PALAVRAS_CHAVE: str
    DATA_INICIO: str
    DATA_FIM: str
    INTIMADO: str
    DOC_SEPARADOR: str
    TRAZER_TEOR: str
    USE_GPT: str
    TRAZER_PDF: str


class PJeMovimentacao(Movimentacao): ...


class ProjudiMovimentacao(Movimentacao): ...


class EsajMovimentacao(Movimentacao): ...
