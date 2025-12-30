"""Autenticador Elaw."""

from __future__ import annotations

from time import sleep

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec

from backend.resources.auth.main import AutenticadorBot


class AutenticadorElaw(AutenticadorBot):
    """Implemente autenticação para o sistema Elaw."""

    def __call__(self) -> bool:
        """Realize o login no sistema Elaw e retorne se foi bem-sucedido.

        Returns:
            bool: Indica se o login foi realizado com sucesso.

        """
        self.driver.get("https://amazonas.elaw.com.br/login")

        # Aguarda até que a página carregue o campo de usuário
        username = self.wait.until(
            ec.presence_of_element_located((By.ID, "username")),
        )
        username.send_keys(self.credenciais.username)

        # Aguarda até que a página carregue o campo de senha
        password = self.wait.until(
            ec.presence_of_element_located((
                By.CSS_SELECTOR,
                "#authKey",
            )),
        )
        password.send_keys(self.credenciais.password)

        # Aguarda até que o botão de entrar esteja disponível
        entrar = self.wait.until(
            ec.presence_of_element_located((By.ID, "j_id_c_1_5_f")),
        )
        entrar.click()

        sleep(7)

        url = self.driver.current_url
        return url != "https://amazonas.elaw.com.br/login"
