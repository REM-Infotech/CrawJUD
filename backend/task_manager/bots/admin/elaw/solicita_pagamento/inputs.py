"""Gerencie o preenchimento de campos para solicitações de pagamento.

Este módulo contém a classe Inputs, responsável por preencher
campos de formulários no sistema de pagamentos automatizados.
"""

from __future__ import annotations

from contextlib import suppress
from typing import TYPE_CHECKING, Literal

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec

from backend.task_manager.resources.elements.elaw import (
    SolicitaPagamento as Element,
)
from backend.task_manager.resources.formatadores import formata_string

from .properties import Geral

if TYPE_CHECKING:
    from backend.task_manager.resources.driver import (
        WebElementBot as WebElement,
    )


type TipoDocumento = Literal["Gru - Custas Processuais", "Guia de Pagamento"]


class Inputs(Geral):
    """Gerencie o preenchimento dos campos de pagamento no sistema."""

    def informa_valor(self, element_input: str) -> None:
        """Preencha o valor da guia de condenação no campo correto.

        Args:
            element_input (str): XPath do campo de valor a ser preenchido.

        """
        # Exibe mensagem de início do preenchimento do valor
        message = "Informando valor da guia"
        message_type = "info"
        self.print_message(message=message, message_type=message_type)

        # Obtém o valor da guia dos dados do bot
        valor_guia = self.bot_data["VALOR_GUIA"]

        # Localiza o campo de valor da condenação na página
        campo_valor: WebElement = self.wait.until(
            ec.presence_of_element_located((
                By.XPATH,
                element_input,
            )),
        )

        # Preenche o campo com o valor e remove o foco
        campo_valor.send_keys(valor_guia)
        campo_valor.blur()

        # Aguarda o carregamento após o preenchimento
        self.sleep_load(Element.CSS_LOAD)

        # Exibe mensagem de sucesso após informar o valor
        message = "Valor informado!"
        message_type = "success"
        self.print_message(message=message, message_type=message_type)

    def informa_descricao(self) -> None:
        """Insira a descrição do pagamento no campo apropriado.

        Esta função preenche o campo de descrição do pagamento
        utilizando o valor presente nos dados do bot.
        """
        # Exibe mensagem de início do preenchimento da descrição
        message = "Inserindo descrição do pagamento"
        message_type = "log"
        self.print_message(message=message, message_type=message_type)

        # Obtém a descrição do pagamento dos dados do bot
        descricao_pgto = self.bot_data["DESC_PAGAMENTO"]

        # Localiza o campo de descrição do pagamento na página
        campo_descricao_pgto: WebElement = self.wait.until(
            ec.presence_of_element_located((
                By.XPATH,
                Element.XPATH_DESCRICAO_PGTO,
            )),
        )

        # Preenche o campo com a descrição e aguarda carregamento
        campo_descricao_pgto.send_keys(descricao_pgto)
        self.sleep_load(Element.CSS_LOAD)

        # Exibe mensagem de sucesso após informar a descrição
        message = "Descrição inserida!"
        message_type = "success"
        self.print_message(message=message, message_type=message_type)

    def informa_data_vencimento(self) -> None:
        """Preencha a data de vencimento no campo correspondente.

        Esta função insere a data de vencimento do pagamento
        conforme os dados fornecidos pelo bot.
        """
        # Exibe mensagem de início do preenchimento da data
        message = "Inserindo data para pagamento"
        message_type = "log"
        self.print_message(message=message, message_type=message_type)

        # Obtém a data de vencimento dos dados do bot
        data_vencimento: str = self.bot_data["DATA_LANCAMENTO"]

        # Localiza o campo de data de vencimento na página
        campo_data_vencimento: WebElement = self.wait.until(
            ec.presence_of_element_located((
                By.XPATH,
                Element.XPATH_DATA_VENCIMENTO,
            )),
        )

        # Preenche o campo com a data e remove o foco
        campo_data_vencimento.send_keys(data_vencimento)
        campo_data_vencimento.blur()
        self.sleep_load(Element.CSS_LOAD)

        # Exibe mensagem de sucesso após informar a data
        message = "Data para pagamento inserido!"
        message_type = "success"
        self.print_message(message=message, message_type=message_type)

    def informa_favorecido(self, cnpj_favorecido: str) -> None:
        """Informe o CNPJ do favorecido no campo apropriado.

        Args:
            cnpj_favorecido (str): CNPJ do favorecido.

        """
        # Exibe mensagem de início do preenchimento do favorecido
        message: str = "Inserindo favorecido"
        message_type: str = "log"
        self.print_message(message=message, message_type=message_type)

        # Localiza o campo de favorecido na página
        campo_input_favorecido: WebElement = self.wait.until(
            ec.presence_of_element_located((
                By.XPATH,
                Element.XPATH_INPUT_FAVORECIDO,
            )),
        )

        # Limpa o campo e aguarda carregamento
        campo_input_favorecido.clear()
        self.sleep_load(Element.CSS_LOAD)

        # Preenche o campo com o CNPJ do favorecido
        campo_input_favorecido.send_keys(cnpj_favorecido)

        # Seleciona o favorecido sugerido na lista
        favorecido: WebElement = self.wait.until(
            ec.presence_of_element_located((
                By.XPATH,
                Element.XPATH_INFO_FAVORECIDO,
            )),
        )
        favorecido.click()
        self.sleep_load(Element.CSS_LOAD)

        # Remove o foco do campo e aguarda carregamento
        campo_input_favorecido.blur()
        self.sleep_load(Element.CSS_LOAD)

        # Exibe mensagem de sucesso após inserir o favorecido
        message = "Favorecido inserido!"
        message_type = "success"
        self.print_message(message=message, message_type=message_type)

    def informa_centro_custa(self, centro_custa: str) -> None:
        """Preencha o centro de custas no campo correspondente.

        Args:
            centro_custa (str): Valor do centro de custas.

        """
        # Exibe mensagem de início do preenchimento do centro de custas
        message: str = "Informando o centro de custas"
        message_type: str = "log"
        self.print_message(message=message, message_type=message_type)

        # Localiza o campo de centro de custas na página
        input_centro_custa: WebElement = self.wait.until(
            ec.presence_of_element_located((
                By.XPATH,
                Element.XPATH_INPUT_CENTRO_CUSTA,
            )),
        )

        # Preenche o campo de centro de custas
        input_centro_custa.send_keys(centro_custa)
        # Remove o foco do campo após preencher
        input_centro_custa.blur()
        # Aguarda o carregamento após o preenchimento
        self.sleep_load(Element.CSS_LOAD)

        # Exibe mensagem de sucesso após informar o centro de custas
        message = "Centro de custas informado!"
        message_type = "success"
        self.print_message(message=message, message_type=message_type)

    def upload_files(
        self,
        arquivos: list[str],
        tipo_documento: TipoDocumento,
    ) -> None:
        """Realize o upload de arquivos para o sistema Elaw.

        Args:
            arquivos (list[str]): Lista de nomes dos arquivos.
            tipo_documento (TipoDocumento): Tipo do documento a ser enviado.
            elemento_input_file (str): XPath do campo de upload.

        """
        # Exibe mensagem de início do envio dos arquivos
        message: str = "Enviando arquivos"
        message_type: str = "log"
        self.print_message(message=message, message_type=message_type)

        elemento_input_file = Element.XPATH_INPUT_UPLOAD_FILE
        elemento_tipo_arquivo = Element.XPATH_SELECT_TIPO_ARQUIVO
        # Faz o upload de cada arquivo
        out_dir = self.output_dir_path
        for arquivo in arquivos:
            message = f'Enviando arquivo "{arquivo}"'
            message_type = "log"
            self.print_message(message=message, message_type=message_type)
            with suppress(Exception):
                # Seleciona o tipo de arquivo no sistemas
                locator = (By.XPATH, elemento_tipo_arquivo)
                predicate = ec.presence_of_element_located(locator)
                campo_tipo_arquivo: WebElement = self.wait.until(predicate)

                campo_tipo_arquivo.select2(tipo_documento)
                self.sleep_load(Element.CSS_LOAD)

            # Normaliza o nome do arquivo e monta o caminho
            nome_normalizado: str = formata_string(arquivo)
            caminho_arquivo = out_dir.joinpath(nome_normalizado)

            # Realiza o upload do arquivo
            locator = (By.XPATH, elemento_input_file)
            predicate = ec.presence_of_element_located(locator)
            campo_upload_file: WebElement = self.wait.until(predicate)

            campo_upload_file.send_file(caminho_arquivo)

            # Aguarda o upload e o carregamento da página
            self.wait_fileupload()
            self.sleep_load(Element.CSS_LOAD)

            # Mensagem de sucesso para cada arquivo enviado
            message = f'Arquivo "{arquivo}" enviado!'
            message_type = "info"
            self.print_message(message=message, message_type=message_type)

        # Mensagem final de sucesso após todos os envios
        message = "Arquivos enviados!"
        message_type = "success"
        self.print_message(message=message, message_type=message_type)
