"""Gerencie inicialização e seleção de pagamentos no Elaw.

Este módulo contém classes e funções para iniciar e selecionar
tipos de pagamento na interface do Elaw.
"""

from __future__ import annotations

import traceback
from time import sleep
from typing import TYPE_CHECKING

from selenium.common import JavascriptException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec

from backend.common.exceptions import ExecutionError
from backend.common.raises import raise_execution_error
from backend.resources.elements.elaw import (
    SolicitaPagamento as Element,
)

from .properties import Geral

if TYPE_CHECKING:
    from .condenacao import PgtoCondenacao
    from .custas import PgtoCustas


class Inicializacao(Geral):
    """Inicialize e gerencie o fluxo de solicitação de pagamento.

    Esta classe controla o acesso, criação e seleção de tipos de
    pagamento na interface do Elaw.
    """

    def novo_pagamento(self: Inicializacao) -> None:
        """Clique no botão para iniciar novo pagamento no Elaw.

        Esta função aguarda o botão de novo pagamento estar disponível
        e realiza o clique para iniciar o processo.

        """
        try:
            # Aguarda o botão de novo pagamento estar disponível
            btn_novo_pgto = self.wait.until(
                ec.presence_of_element_located((
                    By.CSS_SELECTOR,
                    Element.CSS_BTN_NOVO_PGTO,
                )),
            )
            # Realiza o clique no botão para iniciar novo pagamento
            btn_novo_pgto.click()

        except Exception as e:
            message = "\n".join(traceback.format_exception(e))
            raise ExecutionError(message=message) from e

    def seleciona_tipo_pgto(self: Inicializacao) -> PgtoCustas | PgtoCondenacao:
        """Seleciona o tipo de pagamento no formulário do Elaw.

        Returns:
            (PgtoCustas | PgtoCondenacao): Solicitador do tipo de pagamento.

        """
        # Define mensagem de status para logs ou exceções
        message = "Selecionando tipo de pagamento"

        try:
            # Obtém o tipo de pagamento do dicionário de dados do bot
            tipo_pgto: str = self.bot_data["TIPO_PAGAMENTO"].capitalize()
            # Aguarda o elemento do tipo de pagamento estar disponível
            sleep(0.5)
            el_select = self.wait.until(
                ec.presence_of_element_located((
                    By.XPATH,
                    Element.XPATH_TIPO_PAGAMENTO,
                )),
            )
            # Seleciona o tipo de pagamento no formulário
            el_select.select2(tipo_pgto)
            # Aguarda o carregamento após seleção
            self.sleep_load(Element.CSS_LOAD)

            # Retorna a instância do solicitador correspondente
            return self.solicitadores(nome=tipo_pgto)

        except KeyError as e:
            # Trata erro de tipo de pagamento não encontrado
            exc = e.args[0]
            message = f'Tipo de pagamento "{exc}" não encontrado!'
            raise_execution_error(message=message, exc=e)

        except JavascriptException as e:
            # Trata erro de execução de JavaScript no navegador
            message = "\n".join(traceback.format_exception(e))
            raise_execution_error(message=message, exc=e)
