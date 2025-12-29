"""Gerencie seletores e ações para o fluxo de solicitação Elaw.

Este módulo contém a classe Seletores, responsável por manipular
elementos e ações na tela de solicitação de pagamento do Elaw.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from backend.resources.elements.elaw import (
    SolicitaPagamento as Element,
)

from .properties import Geral

if TYPE_CHECKING:
    from backend.resources.driver import (
        WebElementBot as WebElement,
    )


class Seletores(Geral):
    """Gerencie seletores e ações para o fluxo de solicitação Elaw."""

    def informa_tipo_condenacao(self) -> None:
        """Informe o tipo de condenação no campo apropriado.

        Esta função seleciona o tipo de condenação (Sentença, Acordão, etc)
        no formulário do sistema Elaw, utilizando os dados do bot.
        """
        # Exibe mensagem de início do preenchimento do tipo de condenação
        message: str = "Informando tipo da condenação (Sentença, Acordão, etc)"
        message_type: str = "log"
        self.print_message(message=message, message_type=message_type)

        # Obtém o tipo de condenação dos dados do bot
        tipo_condenacao: str = self.bot_data["TIPO_CONDENACAO"]

        # Localiza o campo de seleção do tipo de condenação na página
        select_tipo_condenacao: WebElement = self.seletores_informacao[0]

        # Seleciona o tipo de condenação no campo apropriado
        select_tipo_condenacao.select2(tipo_condenacao)
        self.sleep_load(Element.CSS_LOAD)

        # Exibe mensagem de sucesso após informar o tipo de condenação
        message = "Tipo da condenação informado"
        message_type = "success"
        self.print_message(message=message, message_type=message_type)

    def informa_tipo_custa(self) -> None:
        """Informe o tipo de custa no campo correspondente.

        Esta função seleciona o tipo de custa no formulário do Elaw.
        """
        # Obtém o tipo de custa dos dados do bot
        tipo_custa: str = self.bot_data["TIPO_GUIA"]

        # Exibe mensagem de início do preenchimento do tipo de custa
        message: str = f"Informando tipo de custas. Tipo informado: {tipo_custa}"
        message_type: str = "log"
        self.print_message(message=message, message_type=message_type)

        # Seleciona o campo de tipo de custa e informa o valor
        seletor_tipo_custa = self.seletores_informacao[1]
        seletor_tipo_custa.select2(tipo_custa)

        # Exibe mensagem de sucesso após informar o tipo de custa
        message = "Tipo de custas informado!"
        message_type = "success"
        self.print_message(message=message, message_type=message_type)

    def conta_debito(self, conta_debito: str) -> None:
        """Informe a conta de débito no campo correspondente.

        Args:
            conta_debito (str): Conta de débito a ser informada.

        """
        # Exibe mensagem de início do preenchimento da conta para débito
        message: str = "Informando conta para débito"
        message_type: str = "log"
        self.print_message(message=message, message_type=message_type)

        # Seleciona o campo de conta de débito e informa o valor
        seletor_conta_debito: WebElement = self.seletores_informacao[2]

        seletor_conta_debito.select2(conta_debito)
        self.sleep_load(Element.CSS_LOAD)

        # Exibe mensagem de sucesso após informar a conta para débito
        message = "Conta para débito informada!"
        message_type = "success"
        self.print_message(message=message, message_type=message_type)
