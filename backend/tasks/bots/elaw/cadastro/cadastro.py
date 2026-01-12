from __future__ import annotations

from typing import TYPE_CHECKING

from selenium.webdriver.common.by import By

from backend.resources.elements.elaw import ElawCadastroElements as El

from .main import CadastroElaw

if TYPE_CHECKING:
    from backend.dicionarios import ConfigArgsRobo, ElawCadastro


class PreCadastroElaw(CadastroElaw):
    bot_data: ElawCadastro
    name = "pre_cadastro_elaw"

    def run(self, config: ConfigArgsRobo) -> None:

        self.setup(config=config)
        self.execution()

    def execution(self) -> None:

        if self.search():
            msg = "Processo já cadastrado!"
            type_ = "success"
            self.print_message(msg, type_, self.row)

            data_save = self.bot_data
            data_save["MENSAGEM_SUCESSO"] = msg
            self.append_success("Existentes", [data_save])
            return

        btn_newproc = self.driver.find_element(By.CSS_SELECTOR, El.CSS_BTN_NOVO_PROCESSO)
        btn_newproc.click()
        self.cadastrar()
