"""Extração de informações de processos no Projudi.

Este pacote contém classes e funções para automatizar a
coleta de dados processuais do sistema Projudi.
"""

from __future__ import annotations

import json
from base64 import b64encode
from contextlib import suppress
from datetime import datetime
from time import sleep
from typing import TYPE_CHECKING, ClassVar, Self
from uuid import uuid4
from zoneinfo import ZoneInfo

from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support.wait import WebDriverWait

from backend.controllers import ProjudiBot
from backend.dicionarios import ProjudiCapa
from backend.resources.driver.web_element import WebElement

if TYPE_CHECKING:
    from backend.dicionarios import ArgumentosRobo
    from backend.resources.driver import WebElement


class BuscaProcessual(ProjudiBot):
    name: ClassVar[str] = "busca_processual_projudi"

    def run(self, config: ArgumentosRobo) -> None:

        config.update({
            "sistema": "projudi",
            "cookies": b64encode(
                json.dumps({
                    "access_token_cookie": str(uuid4()),
                }).encode(),
            ).decode(),
        })

        self.args = config
        self.setup(config)
        frame = self.execution()
        self.driver.quit()

        capa_projudi = self.bots["capa_projudi"]().setup(config)
        capa_projudi.frame = frame
        capa_projudi.execution()

        return

    def execution(self) -> list[ProjudiCapa]:

        endpoint = "buscaProcessosQualquerInstancia.do?actionType=pesquisar"
        url_busca = f"https://projudi.tjam.jus.br/projudi/processo/{endpoint}"
        self.driver.get(url_busca)
        sleep(2)

        input_nome_parte = self.wait.until(presence_of_element_located((By.NAME, "nomeParte")))
        input_documento_parte = self.wait.until(presence_of_element_located((By.NAME, "cpfCnpj")))

        input_data_inicio = self.wait.until(presence_of_element_located((By.NAME, "dataInicio")))
        input_data_fim = self.wait.until(presence_of_element_located((By.NAME, "dataFim")))

        input_nome_parte.send_keys(self.args["nome_parte"])
        sleep(0.5)
        input_documento_parte.send_keys(self.args["documento_parte"])
        sleep(0.5)

        now = datetime.now(ZoneInfo("America/Sao_Paulo")).strftime("%d/%m/%Y")

        input_data_inicio.send_keys(now)
        sleep(0.5)
        input_data_fim.send_keys(now)
        sleep(0.5)

        css_any_processo = 'input[value="qualquerAdvogado"][name="filtroAdvogado"]'
        self.wait.until(presence_of_element_located((By.CSS_SELECTOR, css_any_processo))).click()

        sleep(0.5)
        self.wait.until(presence_of_element_located((By.NAME, "pesquisarTodos"))).click()

        sleep(0.5)
        self.wait.until(presence_of_element_located((By.ID, "pesquisar"))).click()

        sleep(0.5)

        return self.extrair()

    def extrair(self) -> list[ProjudiCapa]:

        dados: list[ProjudiCapa] = []

        for item in PaginacaoProjudi(self):
            informacoes = item.find_elements(By.TAG_NAME, "td")
            dados.append(
                ProjudiCapa(
                    NUMERO_PROCESSO=informacoes[0].text,
                    GRAU="1",
                    TRAZER_COPIA="sim",
                    TRAZER_MOVIMENTACOES="SIM",
                ),
            )

        return dados


class PaginacaoProjudi:
    _table_data: list[WebElement]
    btn_next: WebElement = None

    def __init__(self, bot: BuscaProcessual) -> None:

        self.bot = bot
        self._index = 0
        self._table_data = []
        self.wait = WebDriverWait(self.bot.driver, 5)

    def __iter__(self) -> Self:

        return self

    def __next__(self) -> WebElement:

        self.atualizar_items()
        item = self._table_data[self._index]
        self._index += 1

        return item

    def atualizar_items(self) -> None:

        if len(self._table_data) == 0:
            self.listar_tabela()

        elif self._index >= len(self._table_data):
            self._index = 0

            if not self.btn_next:
                with suppress(Exception):
                    self.btn_next = self.wait.until(
                        presence_of_element_located((By.CLASS_NAME, "arrowNextOn")),
                    )

                if not self.btn_next:
                    raise StopIteration

            self.btn_next.click()
            self.btn_next = None

            sleep(5)
            self.listar_tabela()

    def listar_tabela(self) -> None:
        self._table_data = []
        result_table = self.bot.wait.until(
            presence_of_element_located((By.CLASS_NAME, "resultTable")),
        )
        table_body = result_table.find_element(By.TAG_NAME, "tbody")
        table_data = table_body.find_elements(
            By.XPATH,
            "//tr[contains(@class, 'odd') or contains(@class, 'even')]",
        )
        self._table_data.extend(table_data)
