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

from backend.controllers.head import CrawJUD
from backend.dicionarios import DataSucesso
from backend.dicionarios.robos._cidades import cidades_amazonas
from backend.resources.auth import AutenticadorElaw
from backend.resources.elements import elaw as el
from backend.resources.search import ElawSearch

if TYPE_CHECKING:
    from pathlib import Path


class ElawBot(CrawJUD):
    """Classe de controle para robôs do Elaw."""

    def __init__(self) -> None:
        """Inicialize o robô Elaw."""
        self.search = ElawSearch(self)
        self.auth = AutenticadorElaw(self)
        super().__init__()

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

    def sleep_load(self) -> None:
        """Aguarde até que o elemento de carregamento desapareça."""
        element = el.XPATH_ELEMENT_LOAD
        while True:
            sleep(0.5)
            load = None
            aria_value = None
            with suppress(TimeoutException):
                load = WebDriverWait(self.driver, 5).until(
                    ec.presence_of_element_located((
                        By.XPATH,
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
                    self.driver
                    .find_element(
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

    def print_comprovante(self, message: str) -> None:
        """Salve comprovante do processo e registre mensagem de sucesso.

        Args:
            message (str): Mensagem a ser exibida no comprovante.

        """
        numero_processo = self.bot_data.get("NUMERO_PROCESSO")
        name_comprovante = f"Comprovante - {numero_processo} - {self.id_execucao}.png"
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
