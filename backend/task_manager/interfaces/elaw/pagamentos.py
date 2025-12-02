"""Defina interfaces de dados para pagamentos do sistema Elaw.

Este módulo contém a classe CondenacaoData para estruturar
informações de pagamentos e condenações processuais.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol, TypedDict

from backend.task_manager.types_app import P

if TYPE_CHECKING:
    from backend.task_manager.types_app.bot import ProcessoCNJ


class ISolicitacaoPagamentos[T](Protocol[P, T]):
    """Defina interface para solicitações de pagamentos Elaw.

    Estruture chamadas para processar pagamentos no sistema.
    """

    def __init__[T](self, bot: T) -> None:
        """Inicialize a interface com o bot do Elaw.

        Args:
            bot (T): Instância do bot para processar pagamentos.

        """

    def __call__(self) -> None:
        """Execute a solicitação de pagamento Elaw."""
        ...


class CondenacaoDataType(TypedDict):
    """Estruture dados de condenação e pagamento do Elaw.

    Esta classe organiza informações de pagamentos
    processuais, como valores, documentos e partes.
    """

    NUMERO_PROCESSO: ProcessoCNJ
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


class CustasDataType(TypedDict):
    """Estruture dados de custas processuais do sistema Elaw.

    Organize informações de guias, valores e partes envolvidas.
    """

    NUMERO_PROCESSO: ProcessoCNJ
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
