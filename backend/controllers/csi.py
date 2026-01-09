"""Módulo para a classe de controle dos robôs PROJUDI."""

from contextlib import suppress

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec

from backend.controllers import CrawJUD
from backend.resources.elements import csi as el


class CsiBot(CrawJUD):
    """Classe de controle para robôs do CSI."""

    @staticmethod
    def search() -> bool:
        """Realiza uma busca no sistema CSI."""
        _url_search = el.url_busca

    def auth(self) -> bool:
        """Realiza autenticação no sistema CSI.

        Returns:
            bool: Indica se a autenticação foi bem-sucedida.

        """
        self.driver.get(el.URL_LOGIN)

        campo_username = self.wait.until(
            ec.presence_of_element_located((
                By.XPATH,
                el.XPATH_CAMPO_USERNAME,
            )),
        )
        campo_username.send_keys(self.credenciais.username)

        campo_password = self.driver.find_element(
            By.XPATH,
            el.XPATH_CAMPO_SENHA,
        )
        campo_password.send_keys(self.credenciais.password)

        btn_entrar = self.driver.find_element(
            By.XPATH,
            el.XPATH_BTN_ENTRAR,
        )
        btn_entrar.click()

        with suppress(Exception):
            self.wait.until(ec.url_to_be(el.URL_CONFIRMA_LOGIN))

            return True

        return False
