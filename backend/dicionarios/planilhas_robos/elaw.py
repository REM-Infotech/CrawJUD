from __future__ import annotations

from .main import BotData


class ElawCondenacao(BotData):
    NUMERO_PROCESSO: str
    DESC_PAGAMENTO: str
    VALOR_GUIA: str
    DATA_LANCAMENTO: str
    TIPO_PAGAMENTO: str
    SOLICITANTE: str
    TIPO_CONDENACAO: str
    COD_BARRAS: str
    DOC_GUIA: str
    DOC_CALCULO: str
    LOCALIZACAO: str
    CNPJ_FAVORECIDO: str
    FORMA_PAGAMENTO: str
    CENTRO_CUSTAS: str
    CONTA_DEBITO: str


class ElawCustas(BotData):
    NUMERO_PROCESSO: str
    TIPO_GUIA: str
    VALOR_GUIA: str
    DATA_LANCAMENTO: str
    TIPO_PAGAMENTO: str
    SOLICITANTE: str
    DESC_PAGAMENTO: str
    COD_BARRAS: str
    DOC_GUIA: str
    LOCALIZACAO: str
    CNPJ_FAVORECIDO: str
    FORMA_PAGAMENTO: str
    CENTRO_CUSTAS: str
    CONTA_DEBITO: str


class ElawCadastro(BotData):
    AREA_DIREITO: str
    SUBAREA_DIREITO: str
    ESFERA: str

    ESTADO: str
    COMARCA: str
    FORO: str
    VARA: str
    EMPRESA: str
    POLO_EMPRESA: str
    POLO_PARTE_CONTRARIA: str
    DOCUMENTO_PARTE: str
    LOCALIZACAO_PROCESSO: str

    TIPO_ACAO: str
    DATA_DISTRIBUICAO: str
    ADVOGADO_RESPONSAVEL: str
    ADVOGADO_CONTRA: str
    OAB_ADVOGADO: str
    ESCRITORIO_EXTERNO: str
    VALOR_CAUSA: str
    CONTIGENCIAMENTO: str
