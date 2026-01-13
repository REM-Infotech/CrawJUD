"""Autenticador PROJUDI."""

from __future__ import annotations

from contextlib import suppress
from time import sleep

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from backend.common.exceptions import (
    ExecutionError,
    LoginSystemError,
)
from backend.resources.auth.pje import AutenticadorBot
from backend.resources.elements import projudi as el


class AutenticadorProjudi(AutenticadorBot):
    """Implemente autenticação no sistema PROJUDI."""

    def __call__(self) -> bool:
        """Autentique usuário no sistema PROJUDI.

        Returns:
            bool: True se login bem-sucedido, False caso contrário.

        Raises:
            LoginSystemError: Se ocorrer erro na autenticação.

        """
        check_login = None
        try:
            self.driver.get(el.url_login)

            sleep(1.5)

            self.driver.refresh()

            username = self.wait.until(
                ec.presence_of_element_located((
                    By.CSS_SELECTOR,
                    el.campo_username,
                )),
            )

            password = self.driver.find_element(
                By.CSS_SELECTOR,
                el.campo_2_login,
            )

            entrar = self.driver.find_element(
                By.CSS_SELECTOR,
                el.btn_entrar,
            )

            username.send_keys(self.credenciais.username)
            password.send_keys(self.credenciais.password)
            entrar.click()

            with suppress(TimeoutException):
                check_login = WebDriverWait(self.driver, 10).until(
                    ec.presence_of_element_located((
                        By.CSS_SELECTOR,
                        el.chk_login,
                    )),
                )

        except ExecutionError as e:
            raise LoginSystemError(exception=e) from e

        return check_login is not None
