"""Gerencie solicitações de pagamento automatizadas no Elaw.

Este módulo contém a classe e funções para processar, validar e
solicitar pagamentos no sistema Elaw, incluindo automação de
formulários, uploads e verificações de dados.
"""

from __future__ import annotations

import traceback

from backend.common.exceptions import ExecutionError
from backend.common.raises import raise_execution_error
from backend.task_manager.resources.formatadores import (
    formata_string as formata_string,
)
from backend.task_manager.resources.iterators.elaw import ElawIterator

from .condenacao import PgtoCondenacao
from .custas import PgtoCustas


class SolicitaPagamento(PgtoCustas, PgtoCondenacao):
    """Gerencie solicitações de pagamento no sistema Elaw.

    Esta classe executa operações automatizadas para solicitar
    pagamentos, preenchendo formulários e validando dados conforme
    necessário.
    """

    _nome_comprovante: str = None

    def __init__(self) -> None:
        """Inicialize a classe e registre os tipos de pagamento."""
        self.Solicitadores["Condenação"] = self.condenacao
        self.Solicitadores["Custas"] = self.custas

        super().__init__()

    def execution(self) -> None:
        """Execute o processamento das solicitações de pagamento.

        Percorra as solicitações, atualize dados e execute a fila.
        """
        self.driver.maximize_window()
        # Itera sobre cada item retornado pelo ElawIterator
        for pos, value in enumerate(ElawIterator(self)):
            self.row = pos + 1  # Atualiza o número da linha atual
            self.bot_data = value  # Atualiza os dados do bot para o item atual
            if self.bot_stopped.is_set():
                # Interrompe o processamento se o bot for parado
                break

            self.queue()  # Processa a solicitação atual

        # Finaliza a execução após processar todas as solicitações
        self.finalizar_execucao()

    def queue(self) -> None:
        """Processa uma solicitação de pagamento da fila no Elaw.

        Executa busca, inicialização e tratamento de exceções para
        cada solicitação de pagamento.
        """
        # Verifica se o processo existe antes de prosseguir
        try:
            if not self.search():
                # Lança exceção se o processo não for encontrado
                raise_execution_error(message="Processo não encontrado!")

            # Loga o início da solicitação
            message = "Inicializando solicitação..."
            message_type = "log"
            self.print_message(message=message, message_type=message_type)

            # Acessa a tela de pagamentos e executa o tipo de pagamento
            self.acesso_tela_pagamentos()
            self.novo_pagamento()
            call_pgto = self.seleciona_tipo_pgto()
            call_pgto()

        except ExecutionError as e:
            # Trata erros de execução e registra o motivo
            msg = "\n".join(traceback.format_exception_only(e))
            message = f"Erro ao executar operação, Erro: {msg}"
            type_log = "error"
            self.print_message(message=message, message_type=type_log)

            # Atualiza os dados do bot com o
            # motivo do erro e salva no worksheet de erros
            self.bot_data.update({"MOTIVO_ERRO": message})
            self.append_error(worksheet="Erros", data_save=[self.bot_data])
