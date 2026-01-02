"""Implemente buscas de processos no sistema Jusds usando Selenium.

Este módulo contém a classe JusdsSearch para automação de buscas
e abertura de processos judiciais no sistema Jusds.
"""

from __future__ import annotations

from contextlib import suppress
from typing import TYPE_CHECKING

from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import (
    element_to_be_clickable,
    presence_of_element_located,
)
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

from backend.resources.elements import jusds as el
from backend.resources.search.main import SearchBot

if TYPE_CHECKING:
    from backend.controllers.jusds import JusdsBot


class JusdsSearch(SearchBot):
    """Realize buscas de processos no sistema Jusds."""

    bot: JusdsBot

    @property
    def main_window(self) -> str:
        return self.bot.main_window

    @main_window.setter
    def main_window(self, val: str) -> None:
        self.bot.main_window = val

    @property
    def window_busca_processo(self) -> str:
        return self.bot.window_busca_processo

    @window_busca_processo.setter
    def window_busca_processo(self, val: str) -> None:
        self.bot.window_busca_processo = val

    def __call__(self) -> bool:
        """Realiza a busca de um processo no sistema Jusds.

        Returns:
            bool: Indica se o processo foi encontrado.

        """
        message = f"Buscando processo {self.bot_data['NUMERO_PROCESSO']}"
        message_type = "log"

        self.print_message(
            message=message,
            message_type=message_type,
        )

        if not self.window_busca_processo:
            not_mainwindow = list(
                filter(
                    lambda x: x != self.main_window,
                    self.driver.window_handles,
                ),
            )

            if not_mainwindow:
                self.driver.switch_to.window(not_mainwindow[0])
                self.window_busca_processo = self.driver.current_window_handle

        elif self.window_busca_processo:
            self.driver.switch_to.window(self.window_busca_processo)

        self.driver.get(el.LINK_CONSULTA_PROCESSO)

        numero_processo = self.bot_data["NUMERO_PROCESSO"]
        wait = WebDriverWait(self.driver, 15)

        wait_select = wait.until(
            presence_of_element_located((
                By.XPATH,
                el.XPATH_SELECT_CAMPO_BUSCA,
            )),
        )

        select = Select(wait_select)
        select.select_by_value("1")

        campo_busca_processo = wait.until(
            presence_of_element_located((
                By.CSS_SELECTOR,
                el.CSS_CAMPO_BUSCA_PROCESSO,
            )),
        )

        campo_busca_processo.send_keys(numero_processo)

        btn_buscar = wait.until(
            presence_of_element_located((
                By.XPATH,
                el.XPATH_BTN_BUSCAR_PROCESSO,
            )),
        )

        btn_buscar.click()

        with suppress(Exception):
            wait.until(
                presence_of_element_located((
                    By.XPATH,
                    el.XPATH_BTN_ENTRA_PROCESSO,
                )),
            )

            with suppress(Exception):
                modal_load = wait.until(
                    presence_of_element_located((
                        By.XPATH,
                        el.XPATH_LOAD_MODAL,
                    )),
                )

                if modal_load:
                    btn_close_modal = wait.until(
                        presence_of_element_located((
                            By.XPATH,
                            el.XPATH_CLOSE_MODAL,
                        )),
                    )
                    btn_close_modal.click()

            btn_entra_processo = wait.until(
                element_to_be_clickable((
                    By.XPATH,
                    el.XPATH_BTN_ENTRA_PROCESSO,
                )),
            )

            btn_entra_processo.click()

            window = list(
                filter(
                    lambda x: x not in {self.window_busca_processo, self.main_window},
                    self.driver.window_handles,
                ),
            )

            self.driver.switch_to.window(window[-1])

            args_url = self.driver.current_url.split("form.jsp?")[1]

            self.driver.close()

            self.driver.switch_to.window(self.window_busca_processo)

            self.driver.get(
                el.URL_INFORMACOES_PROCESSO.format(args_url=args_url),
            )
            message = "Processo encontrado!"
            message_type = "info"
            self.print_message(
                message=message,
                message_type=message_type,
            )
            return True

        message = "Processo não encontrado!"
        message_type = "error"
        self.print_message(
            message=message,
            message_type=message_type,
        )

        return False
