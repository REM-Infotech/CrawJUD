"""Gerencie o pagamento de custas judiciais no sistema Elaw.

Este módulo contém classes e funções para automatizar o fluxo de
pagamento de custas judiciais, incluindo inicialização, validação,
informação de valores, anexos e dados do favorecido.
"""

from __future__ import annotations

import traceback

from backend.common.raises import raise_execution_error
from backend.task_manager.interfaces.elaw.main import ElawData
from backend.task_manager.resources.elements.elaw import PgtoCustas as Element

from .inicializacao import Inicializacao
from .inputs import Inputs
from .seletores import Seletores
from .validacao import Validador

TIPO_DOCUMENTO = "Gru - Custas Processuais"
FAVORECIDO = "04.812.509/0001-90"
CENTRO_CUSTAS = "A906030100"
CONTA_DEBITO = "CUSTAS JUDICIAIS - MONITORIAS"


class PgtoCustas(Inicializacao, Inputs, Seletores, Validador):
    """Gerencie o pagamento de custas judiciais no sistema Elaw.

    Esta classe integra métodos para informar valores, anexar arquivos,
    preencher dados do favorecido, centro de custas e conta de débito.
    """

    def custas(self) -> None:
        """Execute o pagamento das custas judiciais no Elaw.

        Esta função realiza o fluxo completo de pagamento das custas,
        incluindo valor, anexos, favorecido, centro de custas e conta.

        """
        try:
            # Inicializa os dados do bot com tipagem correta
            self.bot_data = ElawData(**self.bot_data)

            # Informa o valor das custas no campo apropriado
            self.informa_valor(Element.XPATH_INPUT_VALOR)

            # Prepara a lista de arquivos para upload
            arquivos: list[dict[str, str]] = [self.bot_data["DOC_GUIA"]]

            # Realiza o upload dos arquivos necessários
            self.upload_files(
                arquivos=arquivos,
                tipo_documento=TIPO_DOCUMENTO,
            )

            # Executa as etapas do fluxo de pagamento
            self.informa_tipo_custa()
            self.informa_descricao()
            self.informa_data_vencimento()
            self.__informa_favorecido()
            self.informa_forma_pagamento()
            self.__informa_centro_custa()
            self.__conta_debito()
            self.salvar_alteracoes()
            self.confirma_salvamento()

        except Exception as e:
            message = "\n".join(traceback.format_exception(e))
            raise_execution_error(message=message, exc=e)

    def __informa_favorecido(self) -> None:
        """Informe o favorecido no campo do formulário.

        Preencha o campo de favorecido com o CNPJ informado ou padrão.
        """
        # Obtém o CNPJ do favorecido dos dados do bot ou usa o padrão
        cnpj_favorecido: str = self.bot_data.get("CNPJ_FAVORECIDO", FAVORECIDO)

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
