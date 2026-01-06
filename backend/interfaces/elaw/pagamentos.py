"""Defina interfaces de dados para pagamentos do sistema Elaw.

Este módulo contém a classe CondenacaoData para estruturar
informações de pagamentos e condenações processuais.
"""

from __future__ import annotations

from typing import Protocol


class ISolicitacaoPagamentos[**P, T](Protocol[P, T]):
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
