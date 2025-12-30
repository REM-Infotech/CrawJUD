"""Implemente validações e manipulações de pagamentos no Elaw."""

from __future__ import annotations

import re
from contextlib import suppress
from time import sleep
from typing import TYPE_CHECKING

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec

from backend.resources.elements.elaw import (
    SolicitaPagamento as Element,
)

from .properties import Geral

if TYPE_CHECKING:
    from backend.resources.driver import (
        WebElement as WebElement,
    )


STATUS_AGUARDANDO_APROVACAO = "Aguardando Aprovação"


class Validador(Geral):
    """Valide e gerencie pagamentos no sistema Elaw.

    Esta classe herda de Geral e implementa métodos
    para salvar, confirmar e validar pagamentos, além de capturar comprovantes
    e manipular elementos da interface do Elaw.
    """

    def salvar_alteracoes(self) -> None:
        """Salve as alterações realizadas no formulário.

        Esta função clica no botão de salvar para registrar as
        alterações feitas no sistema Elaw.
        """
        # Exibe mensagem de início do salvamento das alterações
        message = "Salvando alterações"
        message_type = "info"
        self.print_message(message=message, message_type=message_type)

        # Localiza o botão de salvar na página
        btn_salvar: WebElement = self.wait.until(
            ec.presence_of_element_located((
                By.XPATH,
                Element.XPATH_BTN_SALVAR,
            )),
        )

        # Clica no botão para salvar as alterações
        btn_salvar.click()

    def confirma_salvamento(self) -> None:
        """Confirma o salvamento do pagamento realizado no Elaw.

        Acesse a tela de pagamentos, verifica se o pagamento foi
        registrado corretamente e salva os dados do comprovante.

        """
        # Acessa a tela de pagamentos novamente para garantir contexto correto
        self.acesso_tela_pagamentos()

        # Salva o contexto atual da janela do navegador
        self.current_context = self.driver.current_window_handle

        # Prepara o dicionário com dados do pagamento
        data = {
            "NUMERO_PROCESSO": self.bot_data["NUMERO_PROCESSO"],
            "ID_PAGAMENTO": "Vazio",
            "COMPROVANTE": self.comprovante1,
        }

        # Percorre a lista de pagamentos para encontrar o registro correto
        for pos, pagamento in enumerate(self.listar_pagamentos()):
            table_data_pagamento = pagamento.find_elements(By.TAG_NAME, "td")
            acoes_td = table_data_pagamento[9]
            id_solicitacao = table_data_pagamento[2].text.strip()

            btn_ver = acoes_td.find_element(
                By.XPATH,
                Element.XPATH_BTN_VER_PGTO,
            )

            btn_ver.click()

            # Verifica se o pagamento corresponde ao esperado
            with suppress(Exception):
                if self.verificar_pagamento(pos=pos):
                    data.update({"ID_PAGAMENTO": id_solicitacao})
                    break

        # Caso não encontre o pagamento, informa para verificação manual
        if data["ID_PAGAMENTO"] == "Vazio":
            message = "Não foi possível comprovar pagamento, verificar manualmente"
            message_type = "info"
            self.print_message(
                message=message,
                message_type=message_type,
            )

        # Salva os dados do pagamento realizado com sucesso
        self.append_success(worksheet="Sucessos", data_save=[data])
        message = "Execução Efetuada com sucesso!"
        message_type = "success"
        self.print_message(
            message=message,
            message_type=message_type,
        )

    @classmethod
    def filtrar_pagamentos(cls, element: WebElement) -> bool:
        """Filtre pagamentos com status aguardando aprovação.

        Args:
            element (WebElement): Elemento da linha da tabela.

        Returns:
            bool: True se o status for aguardando aprovação.

        """
        # Obtém os dados da linha da tabela de pagamentos
        table_data_pagamento = element.find_elements(By.TAG_NAME, "td")
        # Verifica o status do pagamento
        status = table_data_pagamento[4].text.strip()
        return status == STATUS_AGUARDANDO_APROVACAO

    def listar_pagamentos(self) -> list[WebElement]:
        """Lista pagamentos filtrando por status aguardando aprovação.

        Returns:
            list[WebElement]: Lista de elementos de pagamentos filtrados.

        """
        # Aguarda o corpo da tabela de pagamentos estar disponível
        pagamentos_tbody = self.wait.until(
            ec.presence_of_element_located((
                By.XPATH,
                Element.XPATH_TBODY_PAGAMENTOS,
            )),
        )
        # Filtra os pagamentos pelo status definido
        return list(
            filter(
                self.filtrar_pagamentos,
                pagamentos_tbody.find_elements(By.TAG_NAME, "tr"),
            ),
        )

    def verificar_pagamento(self, pos: int) -> bool:
        """Verifique se o pagamento corresponde ao código de barras esperado.

        Args:
            pos (int): Posição do pagamento na lista.

        Returns:
            bool: True se o pagamento for confirmado.

        """
        # Obtém o xpath do modal de informações do pagamento
        element: str = Element.XPATH_MODAL_PAGAMENTO_INFO
        element2: str = Element.XPATH_MODAL_PAGAMENTO_DIALOG
        xpath_modal_info_pgto: str = element.format(pos=pos)
        xpath_modal_info_pgto_dialog: str = element2.format(pos=pos)

        # Aguarda o modal de pagamento estar disponível
        dialog_pagamento: WebElement = self.wait.until(
            ec.presence_of_element_located((By.XPATH, xpath_modal_info_pgto)),
        )

        # Localiza o iframe do pagamento e obtém sua URL
        self.frame_pagamento: WebElement = dialog_pagamento.find_element(
            By.TAG_NAME,
            "iframe",
        )
        self.url_pagamento: str = self.frame_pagamento.get_attribute("src")
        self.driver.switch_to.frame(self.frame_pagamento)

        # Monta o xpath do código de barras e remove caracteres não numéricos
        element = Element.XPATH_CODIGO_BARRAS
        codigo_barra: str = re.sub(r"\D", "", self.bot_data["COD_BARRAS"])
        xpath_cod_barra: str = element.format(codigo_barra=codigo_barra)
        codigo_barras_pgto: WebElement = self.driver.find_element(
            By.XPATH,
            xpath_cod_barra,
        )

        codigo_txt_el = codigo_barras_pgto.text
        sleep(0.5)
        # Fecha o modal e retorna ao contexto padrão

        pagamento_solicitado = codigo_txt_el == codigo_barra
        # Compara o texto do código de barras e captura comprovante se igual
        if pagamento_solicitado:
            self.get_screenshot()

        self.fechar_pagamento_info(
            xpath_modal_info_pgto,
            xpath_modal_info_pgto_dialog,
        )

        sleep(0.5)
        return pagamento_solicitado

    def get_screenshot(self) -> None:
        """Capture comprovante de pagamento e salve em arquivo local."""
        # Define o caminho do arquivo do comprovante
        path_comprovante = self.output_dir_path.joinpath(self.comprovante1)

        # Abre nova aba para acessar a página do comprovante
        self.driver.switch_to.new_window("tab")
        self.driver.get(self.url_pagamento)

        # Salva o screenshot do comprovante no arquivo especificado

        path_comprovante.write_bytes(self.driver.get_screenshot_as_png())

        # Fecha a aba do comprovante e retorna ao contexto anterior
        self.driver.close()
        self.driver.switch_to.window(self.current_context)

    def fechar_pagamento_info(
        self,
        xpath_modal_info_pgto_dialog: str,
        xpath_modal_info_pgto: str,
    ) -> None:
        """Feche os modais de pagamento no Elaw.

        Args:
            xpath_modal_info_pgto_dialog (str): XPath do dialog do modal.
            xpath_modal_info_pgto (str): XPath do modal de pagamento.

        """
        # Retorna ao contexto principal do navegador
        self.driver.switch_to.default_content()
        # Aguarda o dialog do modal de pagamento estar disponível
        dialog_pagamento: WebElement = self.wait.until(
            ec.presence_of_element_located((
                By.XPATH,
                xpath_modal_info_pgto_dialog,
            )),
        )

        # Tenta ocultar o dialog do modal usando JavaScript
        with suppress(Exception):
            self.driver.execute_script(
                "$(arguments[0]).hide()",
                dialog_pagamento,
            )

        # Aguarda o modal de pagamento principal estar disponível
        modal_pgto: WebElement = self.wait.until(
            ec.presence_of_element_located((By.XPATH, xpath_modal_info_pgto)),
        )

        # Tenta ocultar o modal principal usando JavaScript
        with suppress(Exception):
            self.driver.execute_script(
                "$(arguments[0]).hide()",
                modal_pgto,
            )
