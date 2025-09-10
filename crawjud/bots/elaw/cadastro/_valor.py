from __future__ import annotations

from time import sleep
from typing import TYPE_CHECKING

from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec

from crawjud.controllers.elaw import ElawBot
from crawjud.custom.task import ContextTask as ContextTask
from crawjud.decorators import shared_task as shared_task
from crawjud.decorators.bot import wrap_cls as wrap_cls
from crawjud.resources.elements import elaw as el

if TYPE_CHECKING:
    from crawjud.utils.webdriver.web_element import WebElementBot as WebElement


class ElawValores(ElawBot):
    def data_distribuicao(self) -> None:
        self.sleep_load('div[id="j_id_4p"]')
        message = "Informando data de distribuição"
        type_log = "log"
        self.print_msg(message=message, type_log=type_log, row=self.row)

        self.sleep_load('div[id="j_id_4p"]')
        data_distribuicao: WebElement = self.wait.until(
            ec.element_to_be_clickable((
                By.CSS_SELECTOR,
                el.css_data_distribuicao,
            )),
            message="Erro ao encontrar elemento",
        )

        data_distribuicao.clear()

        data_distribuicao.send_keys(self.bot_data.get("DATA_DISTRIBUICAO"))
        data_distribuicao.send_keys(Keys.TAB)
        self.sleep_load('div[id="j_id_4p"]')

        message = "Data de distribuição informada!"
        type_log = "info"
        self.print_msg(message=message, type_log=type_log, row=self.row)

    def valor_causa(self) -> None:
        wait = self.wait
        driver = self.driver

        bot_data = self.bot_data

        message = "Informando valor da causa"
        type_log = "log"
        self.print_msg(message=message, type_log=type_log, row=self.row)

        valor_causa: WebElement = wait.until(
            ec.presence_of_element_located((By.XPATH, el.valor_causa)),
            message="Erro ao encontrar elemento",
        )

        valor_causa.click()
        sleep(0.5)
        valor_causa.clear()
        id_valor_causa = valor_causa.get_attribute("id")
        input_valor_causa = f'input[id="{id_valor_causa}"]'
        valor_causa.send_keys(bot_data.get("VALOR_CAUSA"))

        driver.execute_script(
            f"document.querySelector('{input_valor_causa}').blur()",
        )

        self.sleep_load('div[id="j_id_4p"]')

        message = "Valor da causa informado!"
        type_log = "info"
        self.print_msg(message=message, type_log=type_log, row=self.row)

    def data_citacao(self) -> None:
        message = "Informando data de citação"
        type_log = "log"
        self.print_msg(message=message, type_log=type_log, row=self.row)

        data_citacao: WebElement = self.wait.until(
            ec.presence_of_element_located((
                By.XPATH,
                el.data_citacao,
            )),
        )
        data_citacao.clear()
        self.sleep_load('div[id="j_id_4p"]')
        data_citacao.send_keys(self.bot_data.get("DATA_CITACAO"))
        sleep(2)
        id_element = data_citacao.get_attribute("id")
        id_input_css = f'[id="{id_element}"]'
        comando = f"document.querySelector('{id_input_css}').blur()"
        self.driver.execute_script(comando)
        self.sleep_load('div[id="j_id_4p"]')

        message = "Data de citação informada!"
        type_log = "log"
        self.print_msg(message=message, type_log=type_log, row=self.row)
