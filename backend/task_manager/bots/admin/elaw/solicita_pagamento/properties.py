"""Defina propriedades e dados para o bot de solicitação de pagamento.

Este módulo contém a classe Geral, que gerencia
os dados e propriedades necessários para o fluxo de solicitação de
pagamento no contexto do bot Elaw.
"""

from __future__ import annotations

import traceback
from typing import TYPE_CHECKING, ClassVar

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec

from backend.common.raises import raise_execution_error
from backend.controllers import ElawBot
from backend.resources.elements.elaw import (
    SolicitaPagamento as Element,
)

if TYPE_CHECKING:
    from backend.interfaces.elaw.pagamentos import (
        CondenacaoDataType,
        CustasDataType,
        ISolicitacaoPagamentos,
    )
    from backend.resources.driver.web_element import (
        WebElement as WebElement,
    )

PGTO_BOLETO = "Boleto bancário"


class Geral(ElawBot):
    """Gerencie dados e ações do fluxo de solicitação de pagamento Elaw."""

    _bot_data: CondenacaoDataType | CustasDataType = None
    Solicitadores: ClassVar[dict[str, ISolicitacaoPagamentos]] = {}

    @property
    def bot_data(self) -> CondenacaoDataType | CustasDataType:
        """Retorne os dados do bot para pagamento."""
        return self._bot_data

    @bot_data.setter
    def bot_data(self, val: CondenacaoDataType | CustasDataType) -> None:
        self._bot_data = val

    @property
    def comprovante1(self) -> str:
        """Gere o nome do arquivo do comprovante de pagamento."""
        if not self._nome_comprovante:
            proc = self.bot_data["NUMERO_PROCESSO"]
            pid = self.pid
            now = self.now
            self._nome_comprovante = f"Comprovante {proc} - {pid} - {now}.png"

        return self._nome_comprovante

    def acesso_tela_pagamentos(self) -> None:
        """Acesse a tela de pagamentos do Elaw e clique em novo pagamento.

        Esta função navega até a tela de pagamentos e inicia um novo
        processo de solicitação de pagamento.
        """
        try:
            # Aguarda o botão de acesso à tela de pagamentos estar disponível
            btn_acesso_tela_pgto = self.wait.until(
                ec.presence_of_element_located((
                    By.XPATH,
                    Element.XPATH_BTN_TELA_PGTO,
                )),
            )
            btn_acesso_tela_pgto.click()
            # Aguarda o carregamento do modal do processo
            self.sleep_load(Element.CSS_MODAL_LOAD_PROCESSOVIEW)

        except Exception as e:
            message = "\n".join(traceback.format_exception(e))
            raise_execution_error(message=message, exc=e)

    @property
    def seletores_informacao(self) -> list[WebElement]:
        """Obtenha elementos de informação presentes na tela do Elaw."""
        locator = (By.XPATH, Element.XPATH_SELECTS_INFORMACOES)
        predicate = ec.presence_of_all_elements_located(locator)
        return self.wait.until(predicate)

    def informa_forma_pagamento(self) -> None:
        """Insira a forma de pagamento no formulário do Elaw.

        Esta função seleciona e insere a forma de pagamento
        conforme os dados fornecidos pelo usuário.
        """
        # Exibe mensagem de início do preenchimento da forma de pagamento
        message: str = "Inserindo informações de pagamento"
        message_type: str = "log"
        self.print_message(message=message, message_type=message_type)

        # Obtém o tipo de pagamento dos dados do bot ou usa o padrão
        tipo_pgto: str = self.bot_data.get("FORMA_PAGAMENTO", PGTO_BOLETO)

        # Localiza o seletor de forma de pagamento na página
        seletor_forma_pagamento: WebElement = self.wait.until(
            ec.presence_of_element_located((
                By.XPATH,
                Element.XPATH_SELECT_FORMA_PGTO,
            )),
        )

        # Seleciona o tipo de pagamento no seletor
        seletor_forma_pagamento.select2(tipo_pgto)
        self.sleep_load(Element.CSS_LOAD)

        # Se for boleto bancário, insere o código de barras
        if tipo_pgto == PGTO_BOLETO:
            self.boleto_bancario()

        # Exibe mensagem de sucesso ao finalizar o preenchimento
        message = "Informações de pagamento inseridas!"
        message_type = "success"
        self.print_message(message=message, message_type=message_type)

    def boleto_bancario(self) -> None:
        """Insira o código de barras do boleto bancário no Elaw.

        Esta função preenche o campo de código de barras do boleto
        bancário no sistema Elaw, utilizando o valor fornecido nos
        dados do bot.

        """
        # Exibe mensagem de início do preenchimento do código de barras
        message: str = "Inserindo código de barras do boleto"
        message_type: str = "log"
        self.print_message(message=message, message_type=message_type)

        # Obtém o código de barras dos dados do bot
        codigo_barras: str | None = self.bot_data.get("COD_BARRAS")

        # Localiza o campo de código de barras na página
        input_codigo_barras: WebElement = self.wait.until(
            ec.presence_of_element_located((
                By.XPATH,
                Element.XPATH_INPUT_CODIGO_BARRAS,
            )),
        )

        # Preenche o campo com o código de barras e remove o foco
        input_codigo_barras.send_keys(codigo_barras)
        input_codigo_barras.blur()
        self.sleep_load(Element.CSS_LOAD)

        # Exibe mensagem de sucesso ao inserir o código de barras
        message = "Código de barras inserido!"
        message_type = "info"
        self.print_message(message=message, message_type=message_type)
