"""Define bot para solicitação de pagamento de condenação no Elaw."""

from __future__ import annotations

import traceback

from backend.task_manager.common.raises import raise_execution_error
from backend.task_manager.interfaces.elaw.main import ElawData
from backend.task_manager.resources.elements.elaw import (
    PgtoCondenacao as Element,
)

from .inicializacao import Inicializacao
from .inputs import Inputs
from .seletores import Seletores
from .validacao import Validador

CNPJ_TJAM = "00.360.305/0001-04"
CONTA_DEBITO = "AMAZONAS - PAGTO CONDENAÇÕES DE LITÍGIOS CÍVEIS CONTRAPARTIDA"
PGTO_BOLETO = "Boleto bancário"
CENTRO_CUSTAS = "A906030100"
TIPO_DOCUMENTO = "Guia de Pagamento"


class PgtoCondenacao(Inicializacao, Inputs, Seletores, Validador):
    """Gerencia solicitação de pagamento de condenação no Elaw."""

    def condenacao(self) -> None:
        """Execute a solicitação de pagamento de condenação no Elaw."""
        try:
            self.bot_data = ElawData(**self.bot_data)
            self.informa_valor(
                Element.XPATH_INPUT_VALOR_CONDENACAO,
            )
            self.__envia_arquivos()
            self.informa_tipo_condenacao()
            self.informa_descricao()
            self.informa_data_vencimento()
            self.__informa_favorecido()
            self.informa_forma_pagamento()
            self.__informa_centro_custa()
            self.__conta_debito()
            self.salvar_alteracoes()
            self.confirma_salvamento()

        except Exception as e:
            exc = "\n".join(traceback.format_exception(e))
            raise_execution_error(message=exc, exc=e)

    def __envia_arquivos(self) -> None:
        """Envie arquivos necessários para o pagamento da condenação.

        Esta função faz o upload dos arquivos de guia de pagamento e
        cálculo, caso existam, utilizando os elementos da interface
        do sistema Elaw.
        """
        # Cria lista de arquivos a serem enviados
        arquivos: list[dict[str, str]] = [self.bot_data["DOC_GUIA"]]

        # Verifica se há documento de cálculo adicional

        doc_calculo: str | None = self.bot_data.get("DOC_CALCULO")
        if doc_calculo:
            docs_calculo: list[str] = (
                doc_calculo.split(",") if "," in doc_calculo else [doc_calculo]
            )
            arquivos.extend(docs_calculo)

        self.upload_files(
            arquivos=arquivos,
            tipo_documento=TIPO_DOCUMENTO,
        )

    def __informa_favorecido(self) -> None:
        """Informe o favorecido no campo do formulário.

        Preencha o campo de favorecido com o CNPJ informado ou padrão.
        """
        # Obtém o CNPJ do favorecido dos dados do bot ou usa o padrão
        cnpj_favorecido: str = self.bot_data.get("CNPJ_FAVORECIDO", CNPJ_TJAM)

        self.informa_favorecido(cnpj_favorecido=cnpj_favorecido)

    def __informa_centro_custa(self) -> None:
        """Informe o centro de custas no campo correspondente.

        Esta função preenche o campo de centro de custas utilizando
        os dados fornecidos pelo bot ou o valor padrão.
        """
        # Obtém o centro de custas dos dados do bot ou usa o padrão
        centro_custa: str = self.bot_data.get("CENTRO_CUSTAS", CENTRO_CUSTAS)

        self.informa_centro_custa(centro_custa=centro_custa)

    def __conta_debito(self) -> None:
        """Informe a conta para débito no campo correspondente.

        Esta função seleciona a conta de débito no formulário do sistema
        Elaw, utilizando os dados fornecidos pelo bot ou o valor padrão.

        """
        # Obtém a conta de débito dos dados do bot ou usa o padrão
        conta_debito: str = self.bot_data.get("CONTA_DEBITO", CONTA_DEBITO)

        self.conta_debito(conta_debito=conta_debito)
