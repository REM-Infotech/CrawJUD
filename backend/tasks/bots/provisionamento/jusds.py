# ruff: noqa: BLE001
from __future__ import annotations

from collections import UserString
from contextlib import suppress
from time import sleep
from traceback import format_exception, format_exception_only
from typing import TYPE_CHECKING

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from tqdm import tqdm

from backend.common.exceptions import ExecutionError
from backend.controllers.jusds import JusdsBot
from backend.resources.elements.jusds import Provisionamento as El

if TYPE_CHECKING:
    from backend.controllers.head import BotIterator
    from backend.dicionarios import JusdsProvisionamento
    from backend.resources.driver.web_element import WebElement


STATUS_EVENTO = {
    "FORMALIZADO": "Formalizado",
    "NÃO FORMALIZADO": "Não formalizado",
    "CANCELADO": "Cancelado",
}

NIVEIS = {
    "ALTO": "0",
    "MEDIO": "1",
    "BAIXO": "2",
}

ELEMENTOS = {
    "PARTE": El.CSS_INPUT_PARTE,
    "MOMENTO_PROCESSUAL": El.CSS_INPUT_MOMENTO_PROCESSUAL,
    "ORIGEM_RISCO": El.CSS_INPUT_ORIGEM_RISCO,
    "CRITERIO_DETERMINANTE": El.CSS_INPUT_CRITERIO_DETERMINANTE,
    "VALOR_RISCO": El.CSS_INPUT_VALOR_RISCO,
    "INDICE": El.CSS_INPUT_INDICE,
    "DATA_BASE": El.CSS_INPUT_DATA_BASE,
    "VALOR_PAGO": El.CSS_INPUT_VALOR_PAGO,
    "DATA_PAGAMENTO": El.CSS_INPUT_DATA_PAGAMENTO,
}


class JusdsURL(UserString):
    BASE = "https://infraero.jusds.com.br/JRD/openform.do"

    def __init__(
        self,
        *,
        sys: str,
        action: str,
        formID: str,  # noqa: N803
        mode: str,
        goto: str,
        filter_val: str,
        scrolling: str,
    ) -> None:

        self.sys = sys
        self.action = action
        self.formID = formID
        self.mode = mode
        self.goto = goto
        self.filter = filter_val
        self.scrolling = scrolling

    def __str__(self) -> str:
        return (
            f"{self.BASE}"
            f"?sys={self.sys}"
            f"&action={self.action}"
            f"&formID={self.formID}"
            f"&mode={self.mode}"
            f"&goto={self.goto}"
            f"&filter={self.filter}"
            f"&scrolling={self.scrolling}"
            f"#!"
        )


class Provisionamento(JusdsBot):
    name = "jusds_provisionamento"

    def execution(self) -> None:
        self.driver.maximize_window()
        list_item: BotIterator[JusdsProvisionamento] = self.frame
        for pos, item in enumerate(list_item):
            self.bot_data = item
            self.row = pos + 1
            self.queue()

        self.finalizar_execucao()

    def queue(self) -> None:

        try:
            if self.search():
                self.alterar_risco()

        except Exception as e:
            exc = format_exception(e)
            tqdm.write("\n".join(exc))

            self.print_message(
                message=f"Erro de execução: {exc}",
                message_type="error",
                row=self.row,
            )

            self.append_error(
                "Erros",
                data_save=[
                    {
                        "NUMERO_PROCESSO": self.bot_data["NUMERO_PROCESSO"],
                        "ERRO": "\n".join(format_exception_only(e)),
                    },
                ],
            )

    def alterar_risco(self) -> None:

        proc = self.bot_data["NUMERO_PROCESSO"]
        self.acessa_pagina_risco()

        sleep(2)

        btn_novo_risco = self.wait.until(
            presence_of_element_located((
                By.XPATH,
                '//*[@id="TMAKERGRID9bar"]/i[@id="addButton"]',
            )),
        )

        btn_novo_risco.click()
        id_risco = None
        try:
            self._informa_nivel()

            self._informa_campos()

            self._informa_status()  # ultimo

            self.salva_alteracoes()

            id_risco = self._informa_objeto()

            out = self.output_dir_path
            comprovante = out.joinpath(f"Comprovante - {proc} - {self.id_execucao}.png")
            comprovante.write_bytes(self.driver.get_screenshot_as_png())

            self.append_success(
                "Sucessos",
                [
                    {
                        "NUMERO_PROCESSO": self.bot_data["NUMERO_PROCESSO"],
                        "ID_PROVISAO": id_risco,
                    },
                ],
            )

            type_ = "success"
            msg_ = "Execução efetuada com sucesso!"
            self.print_message(msg_, type_, self.row)

        except Exception as e:
            raise ExecutionError(message="Erro de operação", exc=e) from e

    def _informa_nivel(self) -> None:

        value = NIVEIS[self.bot_data["NIVEL"].upper()]
        input_nivel = self.wait.until(
            presence_of_element_located((By.CSS_SELECTOR, El.CSS_INPUT_NIVEL)),
        )

        self.driver.execute_script(
            "arguments[0].value = arguments[1]",
            input_nivel,
            value,
        )

        items_table = (
            self.wait
            .until(presence_of_element_located((By.XPATH, '//table[@id="isc_CCtable"]')))
            .find_element(By.TAG_NAME, "tbody")
            .find_elements(By.TAG_NAME, "tr")
        )

        items_table.reverse()
        select_element = Select(
            items_table[0]
            .find_elements(By.TAG_NAME, "td")[0]
            .find_element(By.TAG_NAME, "select"),
        )
        select_element.select_by_value(value)

    def _informa_status(self) -> None:

        value = STATUS_EVENTO[self.bot_data["STATUS_EVENTO"].upper()]
        input_status = self.wait.until(
            presence_of_element_located((By.CSS_SELECTOR, El.CSS_INPUT_STATUS_EVENTO)),
        )

        self.driver.execute_script(
            "arguments[0].value = arguments[1]",
            input_status,
            value,
        )

        items_table = (
            self.wait
            .until(presence_of_element_located((By.XPATH, '//table[@id="isc_CCtable"]')))
            .find_element(By.TAG_NAME, "tbody")
            .find_elements(By.TAG_NAME, "tr")
        )
        items_table.reverse()

        tds = list(items_table[0].find_elements(By.TAG_NAME, "td"))
        tds.reverse()
        table_data = tds[0].find_elements(By.TAG_NAME, "div")[1]

        select_element = Select(
            table_data.find_element(By.TAG_NAME, "select"),
        )
        select_element.select_by_value(value)

    def _informa_campos(self) -> None:

        for nome in ELEMENTOS:
            el = self.driver.find_element(By.CSS_SELECTOR, ELEMENTOS[nome])

            val = "SELIC"
            if nome != "INDICE":
                val = str(self.bot_data[nome])

            if nome == "MOMENTO_PROCESSUAL":
                val = self.bot_data[nome].upper()

            self.send_data(val, el)

    def _informa_objeto(self) -> str:

        self.driver.refresh()
        self.acessa_pagina_risco()

        items_table = (
            self.wait
            .until(presence_of_element_located((By.XPATH, '//table[@id="isc_CCtable"]')))
            .find_element(By.TAG_NAME, "tbody")
            .find_elements(By.TAG_NAME, "tr")
        )

        id_risco = (
            items_table[0]
            .find_element(
                By.XPATH,
                '//td[@height="33"][@class="grid" or @class="gridAltCol"]/div',
            )
            .text.strip()
        )

        window_processo = self.driver.current_window_handle
        self.driver.switch_to.new_window("tab")

        self._criacao_objeto(id_risco=id_risco)

        self.driver.close()
        self.driver.switch_to.window(window_processo)

        return id_risco

    def _criacao_objeto(self, id_risco: str) -> None:

        url = str(
            JusdsURL(
                sys="JRD",
                action="openform",
                formID="464569307",
                mode="-1",
                goto="-1",
                filter_val=f"jrd_riscos_processo.jrd_rsp_id={id_risco}@long",
                scrolling="yes",
            ),
        )
        self.driver.get(url)

        adicionar_risco_btn = self.wait.until(
            presence_of_element_located((
                By.XPATH,
                '//*[@id="TMAKERGRIDbar"]/*[@id="addButton"]',
            )),
        )

        adicionar_risco_btn.click()

        input_objeto_risco = self.wait.until(
            presence_of_element_located((By.CSS_SELECTOR, El.CSS_INPUT_OBJETO)),
        )

        self.send_data(self.bot_data["OBJETO_RISCO"].upper(), input_objeto_risco)

        input_objeto_porcentagem = self.wait.until(
            presence_of_element_located((By.CSS_SELECTOR, El.CSS_INPUT_PORCENTAGEM_OBJETO)),
        )

        self.send_data(self.bot_data["OBJETO_PORCENTAGEM"], input_objeto_porcentagem)

        btn_salvar = self.wait.until(
            presence_of_element_located((By.CSS_SELECTOR, El.CSS_BTN_SALVAR_OBJETO)),
        )
        btn_salvar.click()

        sleep(2)

    def acessa_pagina_risco(self) -> None:

        btn_pagina_risco = self.wait.until(
            presence_of_element_located((By.XPATH, '//*[@id="tabButton8"]')),
        )

        with suppress(Exception):
            w = WebDriverWait(self.driver, 10)
            message_popup = w.until(
                presence_of_element_located((
                    By.XPATH,
                    '//*[@id="0143FB23-78A2-4DC4-9ADE-22B059AAEB88"]/div[7]',
                )),
            )

            self.driver.execute_script("$(arguments[0]).toggle()", message_popup)

        with suppress(Exception):
            btn_pagina_risco.click()

    def salva_alteracoes(self) -> None:

        btn_salvar = self.wait.until(
            presence_of_element_located((
                By.XPATH,
                '//div[@id="TMAKERGRID9bar"]/i[@id="saveButton"]',
            )),
        )

        btn_salvar.click()

        sleep(2)

    def send_data(self, val: str, el: WebElement) -> None:

        sleep(0.25)
        el.send_keys(val)
        sleep(2)
        el.send_keys(Keys.ENTER)
        sleep(1)

        with suppress(Exception):
            self.driver.execute_script("return $(arguments[0]).blur()", el)
