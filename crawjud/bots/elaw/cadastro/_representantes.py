from __future__ import annotations

from contextlib import suppress
from time import sleep
from typing import TYPE_CHECKING

from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from crawjud.common import _raise_execution_error
from crawjud.controllers.elaw import ElawBot
from crawjud.custom.task import ContextTask as ContextTask
from crawjud.decorators import shared_task as shared_task
from crawjud.decorators.bot import wrap_cls as wrap_cls
from crawjud.resources.elements import elaw as el

if TYPE_CHECKING:
    from crawjud.utils.webdriver.web_element import WebElementBot as WebElement


class ElawRepresentantes(ElawBot):
    def adv_parte_contraria(self) -> None:
        driver = self.driver
        wait = self.wait

        bot_data = self.bot_data
        message = "Informando Adv. Parte contrária"
        type_log = "log"
        self.print_msg(message=message, type_log=type_log, row=self.row)

        campo_adv: WebElement = wait.until(
            ec.presence_of_element_located((
                By.CSS_SELECTOR,
                el.css_input_adv,
            )),
            message="Erro ao encontrar elemento",
        )
        campo_adv.click()
        campo_adv.clear()
        sleep(0.02)

        text = str(bot_data.get("ADV_PARTE_CONTRARIA"))

        for i in ["\t", "\n"]:
            if i in text:
                text = text.split(i)[0]
                break

        campo_adv.send_keys(text)

        check_adv = None

        self.sleep_load('div[id="j_id_4b"]')

        with suppress(TimeoutException):
            check_adv = (
                WebDriverWait(driver, 15)
                .until(
                    ec.presence_of_element_located((
                        By.XPATH,
                        el.css_check_adv,
                    )),
                    message="Erro ao encontrar elemento",
                )
                .text
            )
            campo_adv.send_keys(Keys.ENTER)

            element_campo_adv_outraparte = (
                f'input[id="{campo_adv.get_attribute("id")}"]'
            )

            driver.execute_script(
                f"document.querySelector('{element_campo_adv_outraparte}').blur()",
            )

            self.sleep_load('div[id="j_id_4b"]')

            message = "Adv. parte contrária informado!"
            type_log = "info"
            self.print_msg(message=message, type_log=type_log, row=self.row)

            return

        if not check_adv:
            self.cadastro_advogado_contra()
            driver.switch_to.default_content()

        self.sleep_load('div[id="j_id_4b"]')

        message = "Adv. parte contrária informado!"
        type_log = "info"
        self.print_msg(message=message, type_log=type_log, row=self.row)

    def advogado_interno(self) -> None:
        wait = self.wait
        driver = self.driver

        bot_data = self.bot_data

        message = "informando advogado interno"
        type_log = "log"
        self.print_msg(message=message, type_log=type_log, row=self.row)

        input_adv_responsavel: WebElement = wait.until(
            ec.presence_of_element_located((
                By.XPATH,
                el.adv_responsavel,
            )),
        )
        input_adv_responsavel.click()
        input_adv_responsavel.send_keys(
            bot_data.get("ADVOGADO_INTERNO"),
        )

        id_input_adv = input_adv_responsavel.get_attribute("id").replace(
            "_input",
            "_panel",
        )
        css_wait_adv = f"span[id='{id_input_adv}'] > ul > li"

        wait_adv = None

        with suppress(TimeoutException):
            wait_adv: WebElement = WebDriverWait(driver, 25).until(
                ec.presence_of_element_located((
                    By.CSS_SELECTOR,
                    css_wait_adv,
                )),
            )

        if wait_adv:
            wait_adv.click()
        elif not wait_adv:
            _raise_execution_error(message="Advogado interno não encontrado")

        self.sleep_load('div[id="j_id_4b"]')

        self.sleep_load('div[id="j_id_4b"]')
        element_select: WebElement = wait.until(
            ec.presence_of_element_located((
                By.XPATH,
                el.select_advogado_responsavel,
            )),
        )
        element_select.select2(bot_data.get("ADVOGADO_INTERNO"))

        id_element = element_select.get_attribute("id")
        id_input_css = f'[id="{id_element}"]'
        comando = f"document.querySelector('{id_input_css}').blur()"
        driver.execute_script(comando)

        self.sleep_load('div[id="j_id_4b"]')

        message = "Advogado interno informado!"
        type_log = "info"
        self.print_msg(message=message, type_log=type_log, row=self.row)

    def escritorio_externo(self) -> None:
        wait = self.wait
        bot_data = self.bot_data

        message = "Informando Escritório Externo"
        type_log = "log"
        self.print_msg(message=message, type_log=type_log, row=self.row)

        div_escritrorioexterno: WebElement = wait.until(
            ec.presence_of_element_located((
                By.XPATH,
                el.escritrorio_externo,
            )),
            message="Erro ao encontrar elemento",
        )
        div_escritrorioexterno.click()
        sleep(1)

        text = bot_data.get("ESCRITORIO_EXTERNO")
        select_escritorio: WebElement = wait.until(
            ec.presence_of_element_located((
                By.XPATH,
                el.select_escritorio,
            )),
        )
        select_escritorio.select2(text)
        self.sleep_load('div[id="j_id_4b"]')

        message = "Escritório externo informado!"
        type_log = "info"
        self.print_msg(message=message, type_log=type_log, row=self.row)

    def cadastro_advogado_contra(self) -> None:
        try:
            wait = self.wait
            driver = self.driver

            bot_data = self.bot_data

            message = "Cadastrando advogado"
            type_log = "log"
            self.print_msg(message=message, type_log=type_log, row=self.row)

            add_parte: WebElement = wait.until(
                ec.presence_of_element_located((
                    By.XPATH,
                    el.btn_novo_advogado_contra,
                )),
                message="Erro ao encontrar elemento",
            )
            add_parte.click()

            self.sleep_load('div[id="j_id_4b"]')

            main_window = driver.current_window_handle

            iframe: WebElement = WebDriverWait(driver, 10).until(
                ec.presence_of_element_located((
                    By.CSS_SELECTOR,
                    el.iframe_cadastro_advogado_contra,
                )),
                message="Erro ao encontrar elemento",
            )
            link_iframe = iframe.get_attribute("src")
            driver.switch_to.new_window("tab")
            driver.get(link_iframe)

            sleep(0.5)

            naoinfomadoc: WebElement = wait.until(
                ec.presence_of_element_located((
                    By.CSS_SELECTOR,
                    el.css_naoinfomadoc,
                )),
                message="Erro ao encontrar elemento",
            )
            naoinfomadoc.click()

            sleep(0.5)
            continuebutton: WebElement = wait.until(
                ec.presence_of_element_located((
                    By.CSS_SELECTOR,
                    el.botao_continuar,
                )),
                message="Erro ao encontrar elemento",
            )
            continuebutton.click()

            self.sleep_load('div[id="j_id_1o"]')
            sleep(0.5)

            input_nomeadv: WebElement = wait.until(
                ec.presence_of_element_located((
                    By.CSS_SELECTOR,
                    el.css_input_nomeadv,
                )),
                message="Erro ao encontrar elemento",
            )
            input_nomeadv.click()
            input_nomeadv.send_keys(bot_data.get("ADV_PARTE_CONTRARIA"))

            driver.execute_script(
                f"document.querySelector('{el.css_input_nomeadv}').blur()",
            )

            sleep(0.05)
            salvar: WebElement = wait.until(
                ec.presence_of_element_located((
                    By.CSS_SELECTOR,
                    el.salvarcss,
                )),
                message="Erro ao encontrar elemento",
            )
            salvar.click()

            message = "Advogado cadastrado!"
            type_log = "info"
            self.print_msg(message=message, type_log=type_log, row=self.row)

            driver.close()
            driver.switch_to.window(main_window)

            wait.until(
                ec.presence_of_element_located((
                    By.CSS_SELECTOR,
                    el.iframe_cadastro_advogado_close_dnv,
                )),
            )

            self.sleep_load('div[id="j_id_4b"]')

        except Exception:
            message = "Não foi possível cadastrar advogado"
            _raise_execution_error(message=message)

    def check_part_found(self) -> str | None:
        name_parte = None
        tries: int = 0

        driver = self.driver

        while tries < 4:
            with suppress(NoSuchElementException):
                name_parte = (
                    driver.find_element(
                        By.CSS_SELECTOR,
                        el.css_t_found,
                    )
                    .find_element(By.TAG_NAME, "td")
                    .text
                )

            if name_parte:
                break

            sleep(1)
            tries += 1

        return name_parte
