"""Gerencie atualização de fases processuais no sistema ELAW."""

from __future__ import annotations

import traceback
from time import sleep
from typing import TYPE_CHECKING, ClassVar

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec

from backend.common import raise_execution_error
from backend.controllers.elaw import ElawBot
from backend.resources.elements.elaw import AtualizaFase as Element

if TYPE_CHECKING:
    from backend.resources.driver.web_element import WebElement


class AtualizaFase(ElawBot):
    """Gerencie atualização de fase de fases no ELAW.

    Esta classe executa a busca, atualização e confirmação
    de fases processuais conforme parâmetros definidos.
    """

    name: ClassVar[str] = "atualiza_fase_elaw"

    def execution(self) -> None:
        """Execute atualização das fases processuais do ELAW.

        Percorra o frame, atualize e processe cada linha.
        """
        # Itera sobre os dados do frame e processa cada linha
        self.driver.maximize_window()

        for pos, value in enumerate(self.frame):
            self.row = pos + 1
            self.bot_data = value

            self.queue()

        self.finalizar_execucao()

    def queue(self) -> None:
        """Execute busca e atualização de fase processual.

        Tenta localizar o processo e atualizar sua fase;
        registra erro caso não encontre ou ocorra falha.
        """
        # Tenta buscar o processo pelo critério definido
        try:
            search = self.search()
            if not search:
                raise_execution_error(message="Processo não encontrado!")

            # Atualiza a fase processual se encontrado
            self.atualizar()

        except Exception as e:
            message_error = "\n".join(traceback.format_exception(e))

            for stack in traceback.format_exception(e):
                self.print_message(
                    message=stack,
                    message_type="info",
                )

            # Exibe mensagem de erro e registra o motivo
            self.print_message(
                message=f"{message_error}.",
                message_type="error",
            )

            self.bot_data.update({"MOTIVO_ERRO": message_error})
            self.append_error(worksheet="Erros", data_save=[self.bot_data])

    def atualizar(self) -> None:
        """Atualiza fase processual do processo no sistema ELAW.

        Busca e seleciona a nova fase e salva a alteração.
        """
        message = "Atualizando Fase"
        message_type = "log"
        self.print_message(message=message, message_type=message_type)

        # Aguarda o botão de alterar fase estar disponível
        btn_alterar_fase = self.wait.until(
            ec.presence_of_element_located((
                By.XPATH,
                Element.XPATH_BTN_ALTERAR_FASE,
            )),
        )

        # Clica no botão para abrir o formulário de alteração de fase
        btn_alterar_fase.click()

        # Aguarda o formulário de alteração de fase aparecer
        self.wait.until(
            ec.presence_of_element_located((
                By.XPATH,
                Element.XPATH_FORM_ALTERA_FASE,
            )),
        )
        sleep(2)
        # Seleciona a nova fase no seletor apropriado
        seletor_altera_fase: WebElement = self.wait.until(
            ec.presence_of_element_located((
                By.XPATH,
                Element.XPATH_SELETOR_FASE,
            )),
        )

        fase = self.bot_data["FASE"]
        seletor_altera_fase.select2(to_search=fase)
        sleep(2)
        # Aguarda e clica no botão de salvar alteração
        btn_salvar = self.wait.until(
            ec.presence_of_element_located((
                By.XPATH,
                Element.XPATH_BTN_SALVAR,
            )),
        )

        btn_salvar.click()

        # Confirma se a alteração foi realizada com sucesso
        self.confirma_alteracao()

    def confirma_alteracao(self) -> None:
        """Confirma alteração da fase e salve comprovante no ELAW.

        Esta função verifica se a fase foi atualizada corretamente e
        salva um comprovante em formato PNG na pasta de saída.
        """
        sleep(10)
        # Aguarda o formulário de informações do processo estar presente
        form_info_processo = self.wait.until(
            ec.presence_of_element_located((
                By.XPATH,
                Element.XPATH_FORM_INFORMACAO_PROCESSO,
            )),
        )

        # Obtém a fase que deveria ser atualizada e a fase
        # exibida após alteração
        fase_para_atualizar = self.bot_data["FASE"]
        fase_atualizada = self.wait.until(
            ec.presence_of_element_located((
                By.XPATH,
                Element.XPATH_TEXTO_FASE,
            )),
        ).text

        # Verifica se a fase foi realmente atualizada
        if fase_atualizada != fase_para_atualizar:
            raise_execution_error("Fase não atualizada!")

        # Monta o nome do arquivo de comprovante
        pid = self.pid
        out_dir = self.output_dir_path
        processo = self.bot_data["NUMERO_PROCESSO"]
        nome_comprovante = f"COMPROVANTE - {processo} - {pid}.png"

        # Salva o comprovante como imagem PNG
        path_comprovante = out_dir.joinpath(nome_comprovante)
        with path_comprovante.open("wb") as fp:
            fp.write(form_info_processo.screenshot_as_png)

        # Prepara mensagem de sucesso e dados para salvar
        message = "Fase atualizada com sucesso!"
        message_type = "success"

        data_save = [
            {
                "NUMERO_PROCESSO": processo,
                "COMPROVANTE": nome_comprovante,
            },
        ]

        # Exibe mensagem e registra sucesso
        self.print_message(message=message, message_type=message_type)
        self.append_success(worksheet="Sucessos", data_save=data_save)
