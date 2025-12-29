"""Implemente buscas de processos no sistema Jusds usando Selenium.

Este módulo contém a classe JusdsSearch para automação de buscas
e abertura de processos judiciais no sistema Jusds.
"""

from __future__ import annotations

from contextlib import suppress
from time import sleep
from typing import TYPE_CHECKING

from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support.select import Select

from backend.resources.elements import jusds as el
from backend.resources.search.main import SearchBot

if TYPE_CHECKING:
    from backend.resources.driver.web_element import WebElement


class JusdsSearch(SearchBot):
    """Realize buscas de processos no sistema Jusds."""

    def __call__(self) -> bool:
        """Realiza a busca de um processo no sistema Jusds.

        Returns:
            bool: Indica se o processo foi encontrado.

        """
        processo_encontrado = False
        try:
            numero_processo = self.bot_data.get("NUMERO_PROCESSO")
            message = f"Buscando processo {numero_processo}"
            message_type = "log"
            self.print_message(message, message_type)

            self.driver.get(el.LINK_CONSULTA_PROCESSO)

            select_inputs = self.wait.until(
                presence_of_element_located((By.XPATH, el.XPATH_SELECT_CAMPO_BUSCA)),
            )

            Select(select_inputs).select_by_value("1")

            sleep(0.5)

            campo_busca: WebElement = self.wait.until(
                presence_of_element_located((
                    By.CSS_SELECTOR,
                    el.CSS_CAMPO_BUSCA_PROCESSO,
                )),
            )

            campo_busca.send_keys(self.bot_data["NUMERO_PROCESSO"])

            sleep(1)

            self.wait.until(
                presence_of_element_located((By.XPATH, el.XPATH_BTN_BUSCAR_PROCESSO)),
            ).click()

            with suppress(Exception):
                self.wait.until(
                    presence_of_element_located((By.XPATH, el.XPATH_BTN_ENTRA_PROCESSO)),
                ).click()

                processo_encontrado = True

                self.print_message("Processo Encontrado!", "info")

        except Exception:  # noqa: BLE001
            return processo_encontrado

        return processo_encontrado
