"""Módulo para a classe de controle dos robôs Elaw."""

from __future__ import annotations

from contextlib import suppress
from time import sleep
from typing import TYPE_CHECKING

from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from backend.common.raises import raise_execution_error
from backend.controllers.head import CrawJUD
from backend.interfaces import DataSucesso
from backend.resources.auth import AutenticadorElaw
from backend.resources.search import ElawSearch
from backend.task_manager.constants.data._bots.cidades import cidades_amazonas

if TYPE_CHECKING:
    from pathlib import Path

    from backend.resources.driver.web_element import WebElement


class ElawBot(CrawJUD):
    """Classe de controle para robôs do Elaw."""

    def __init__(self) -> None:
        """Inicialize o robô Elaw."""
        self.search = ElawSearch(self)
        self.auth = AutenticadorElaw(self)

    def elaw_formats(self, data: dict[str, str]) -> dict[str, str]:
        """Formata e ajuste os dados para uso no Elaw.

        Args:
            data (dict[str, str]): Dados a serem formatados.

        Returns:
            dict[str, str]: Dados formatados para o Elaw.

        """
        # Remove chaves com valores vazios ou None
        self._remove_empty_keys(data)

        # Atualiza "TIPO_PARTE_CONTRARIA" se necessário
        self._update_tipo_parte_contraria(data)

        # Atualiza "CAPITAL_INTERIOR" conforme "COMARCA"
        self._update_capital_interior(data, cidades_amazonas)

        # Define "DATA_INICIO" se ausente e "DATA_LIMITE" presente
        self._set_data_inicio(data)

        # Formata valores numéricos
        self._format_numeric_values(data)

        # Define "CNPJ_FAVORECIDO" padrão se vazio
        self._set_default_cnpj(data)

        return data

    def sleep_load(self, element: str) -> None:
        """Aguarde até que o elemento de carregamento desapareça."""
        while True:
            sleep(0.5)
            load = None
            aria_value = None
            with suppress(TimeoutException):
                load = WebDriverWait(self.driver, 5).until(
                    ec.presence_of_element_located((
                        By.CSS_SELECTOR,
                        element,
                    )),
                )

            if load:
                with suppress(Exception):
                    for attributes in ["aria-live", "aria-hidden", "class"]:
                        aria_value = load.get_attribute(attributes)

                        if not aria_value:
                            continue

                        break

                    if aria_value is None or any(
                        value == aria_value
                        for value in [
                            "off",
                            "true",
                            "spinner--fullpage spinner--fullpage--show",
                        ]
                    ):
                        break

            if not load:
                break

    def wait_fileupload(self) -> None:
        """Aguarde até que o upload do arquivo seja concluído."""
        while True:
            sleep(0.05)

            progress_bar = None

            with suppress(NoSuchElementException):
                progress_bar = (
                    self.driver.find_element(
                        By.CSS_SELECTOR,
                        'div[id*=":uploadGedEFile"]',
                    )
                    .find_element(
                        By.CSS_SELECTOR,
                        'div[class="ui-fileupload-files"]',
                    )
                    .find_element(
                        By.CSS_SELECTOR,
                        'div[class="ui-fileupload-row"]',
                    )
                )

            if not progress_bar:
                break

    def screenshot_iframe(
        self,
        url_page: str,
        path_comprovante: Path,
    ) -> None:
        """Capture e salve um print da página em um novo iframe.

        Args:
            url_page (str): URL da página a ser capturada.
            path_comprovante (Path): Caminho para salvar o print.

        """
        driver = self.driver
        main_window = driver.current_window_handle

        self.driver.switch_to.new_window("tab")
        self.driver.get(url_page)

        sleep(5)

        bytes_png = self.driver.get_screenshot_as_png()
        path_comprovante.write_bytes(bytes_png)

        self.driver.close()

        self.driver.switch_to.window(main_window)

    def select2(self, element: WebElement, to_search: str) -> None:
        """Selecione uma opção em campo select2 pelo texto informado.

        Args:
            element (WebElement): Elemento select2 alvo.
            to_search (str): Texto da opção a ser selecionada.

        """
        # Busca todas as opções do select2
        items = element.find_elements(By.TAG_NAME, "option")
        opt_itens: dict[str, str] = {}

        # Obtém o id do elemento select
        id_select = element.get_attribute("id")

        # Mapeia o texto das opções para seus valores
        for item in items:
            value_item = item.get_attribute("value")
            cms = f"select[id='{id_select}'] > option[value='{value_item}']"
            text_item = self.driver.execute_script(
                f'return $("{cms}").text();',
            )
            text_item = " ".join([
                item for item in str(text_item).strip().split(" ") if item
            ]).upper()
            opt_itens.update({text_item: value_item})

        # Normaliza o texto de busca
        to_search = " ".join(to_search.split(" ")).upper()
        value_opt = opt_itens.get(to_search)

        # Seleciona a opção se encontrada
        if value_opt:
            css_select = f"select[id='{id_select}']"  # noqa: Q004, RUF100
            command = f'$("{css_select}").val(["{value_opt}"]);'
            command2 = f'$("{css_select}").trigger("change");'

            self.driver.execute_script(command)
            sleep(2)
            self.driver.execute_script(command2)
            sleep(2)
            return

        # Lança exceção se a opção não for encontrada
        raise_execution_error(message=f'Opção "{to_search}" não encontrada!')

    def print_comprovante(self, message: str) -> None:
        """Salve comprovante do processo e registre mensagem de sucesso.

        Args:
            message (str): Mensagem a ser exibida no comprovante.

        """
        numero_processo = self.bot_data.get("NUMERO_PROCESSO")
        name_comprovante = f"Comprovante - {numero_processo} - {self.pid}.png"
        savecomprovante = self.output_dir_path.joinpath(
            name_comprovante,
        )

        with savecomprovante.open("wb") as fp:
            fp.write(self.driver.get_screenshot_as_png())

        data = DataSucesso(
            NUMERO_PROCESSO=numero_processo,
            MENSAGEM=message,
            NOME_COMPROVANTE=name_comprovante,
            NOME_COMPROVANTE_2="",
        )
        self.append_success(worksheet="sucessos", data_save=[data])

        self.print_message(
            message=message,
            message_type="success",
        )
