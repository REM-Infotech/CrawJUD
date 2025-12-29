"""Autenticador Jusds."""

from __future__ import annotations

from contextlib import suppress
from typing import TYPE_CHECKING

from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import (
    presence_of_element_located,
    url_matches,
)

from backend.resources.auth.main import AutenticadorBot
from backend.resources.elements import jusds as el

if TYPE_CHECKING:
    from backend.resources.driver.web_element import WebElement


class AutenticadorJusds(AutenticadorBot):
    """Implemente autenticação para o sistema Jusds."""

    def __call__(self) -> bool:
        """Realize o login no sistema Jusds e retorne se foi bem-sucedido.

        Returns:
            bool: Indica se o login foi realizado com sucesso.

        """
        self.driver.get(el.URL_LOGIN_JUSDS)

        # Aguarda até que a página carregue o campo de usuário

        username: WebElement = self.wait.until(
            presence_of_element_located((By.CSS_SELECTOR, el.CSS_CAMPO_INPUT_LOGIN)),
        )
        username.send_keys(self.credenciais.username)

        # Aguarda até que a página carregue o campo de senha
        password = self.wait.until(
            presence_of_element_located((
                By.CSS_SELECTOR,
                el.CSS_CAMPO_INPUT_SENHA,
            )),
        )
        password.send_keys(self.credenciais.password)

        # Aguarda até que o botão de entrar esteja disponível
        entrar = self.wait.until(
            presence_of_element_located((By.XPATH, el.XPATH_BTN_ENTRAR)),
        )
        entrar.click()

        with suppress(Exception):
            return self.wait.until(url_matches(el.URL_CONFIRMA_LOGIN))

        return False
