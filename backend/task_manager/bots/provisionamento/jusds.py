# ruff: noqa: T201, BLE001
from __future__ import annotations

from time import sleep
from traceback import format_exception
from typing import TYPE_CHECKING, ClassVar, Literal, Self

from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from tqdm import tqdm

from backend.controllers.jusds import JusdsBot
from backend.resources.driver.web_element import WebElement

if TYPE_CHECKING:
    from backend.controllers.head import BotIterator
    from backend.dicionarios import JusdsProvisionamento
    from backend.resources.driver.web_element import WebElement


FIELDS = [
    "NIVEL",
    "GRAU",
    "NUMERO",
    "DATA_AVALIACAO",
    "RESPONSAVEL_AVALIACAO",
    "PARTE",
    "OBJETOS_RISCO",
    "OBSERVACAO",
    "MOMENTO_PROCESSUAL",
    "ORIGEM_RISCO",
    "CRITERIO_DETERMINANTE",
    "VALOR_RISCO",
    "INDICE",
    "DATA_BASE",
    "VALOR_CORRIGIDO",
    "VALOR_PAGO",
    "DATA_PAGAMENTO",
    "SALDO_CORRIGIDO",
    "VALOR_PROVISIONADO",
    "HONORARIOS",
    "VALOR_HONORARIOS",
    "VALOR_PROVISIONADO_FINAL",
    "STATUS_EVENTO",
]

type FielsProvisao = Literal[
    "NIVEL",
    "GRAU",
    "NUMERO",
    "DATA_AVALIACAO",
    "RESPONSAVEL_AVALIACAO",
    "PARTE",
    "OBJETOS_RISCO",
    "OBSERVACAO",
    "MOMENTO_PROCESSUAL",
    "ORIGEM_RISCO",
    "CRITERIO_DETERMINANTE",
    "VALOR_RISCO",
    "INDICE",
    "DATA_BASE",
    "VALOR_CORRIGIDO",
    "VALOR_PAGO",
    "DATA_PAGAMENTO",
    "SALDO_CORRIGIDO",
    "VALOR_PROVISIONADO",
    "HONORARIOS",
    "VALOR_HONORARIOS",
    "VALOR_PROVISIONADO_FINAL",
    "STATUS_EVENTO",
]


class ItemProvisao:
    td_dict: ClassVar[dict[FielsProvisao, WebElement]] = {}

    def __init__(self, table_data: list[WebElement]) -> None:
        self.table_data = table_data
        for pos, item in enumerate(FIELDS):
            self.td_dict.update({item: table_data[pos]})

    def __getitem__(self, key: FielsProvisao) -> WebElement | None:
        return self.td_dict.get(key)

    def __setitem__(self, key: FielsProvisao, value: WebElement) -> None:
        self.td_dict.setdefault(key, value)


class TableProvisao:
    def __init__(self, element: WebElement) -> None:
        self._table = element
        self._index = 0

        colgroup = element.find_element(By.TAG_NAME, "colgroup")
        self.nome_colunas = colgroup.find_elements(By.TAG_NAME, "col")
        self.table_rows = self._table.find_elements(By.TAG_NAME, "tr")

    def __iter__(self) -> Self:
        """Retorne o próprio iterador para permitir iteração sobre regiões.

        Returns:
            RegioesIterator: O próprio iterador de regiões.

        """
        return self

    def __next__(self) -> ItemProvisao:
        """Implementa a iteração retornando próxima região e dados associados.

        Returns:
            tuple[str, str]: Tupla contendo a região e os dados da região.

        Raises:
            StopIteration: Quando todas as regiões forem iteradas.

        """
        table_data = self.table_rows[self._index].find_elements(By.TAG_NAME, "td")
        if self._index >= len(self.table_rows):
            raise StopIteration

        self._index += 1
        return ItemProvisao(table_data=table_data)


class Provisionamento(JusdsBot):
    name = "jusds_provisionamento"

    def execution(self) -> None:

        list_item: BotIterator[JusdsProvisionamento] = self.frame
        for pos, item in enumerate(list_item):
            self.bot_data = item
            self.row = pos
            self.queue()

        self.finalizar_execucao()

    def queue(self) -> None:

        try:
            if self.search():
                self.alterar_risco()

        except Exception as e:
            exc = format_exception(e)
            tqdm.write("\n".join(exc))

    def alterar_risco(self) -> None:

        btn_pagina_risco = self.wait.until(
            presence_of_element_located((By.XPATH, '//*[@id="tabButton8"]')),
        )

        btn_pagina_risco.click()

        sleep(2)

        btn_editar_risco = self.wait.until(
            presence_of_element_located((
                By.XPATH,
                '//*[@id="TMAKERGRID9bar"]/i[@id="editButton"]',
            )),
        )

        table = TableProvisao(
            self.wait.until(
                presence_of_element_located((By.XPATH, '//*[@id="isc_C6table"]')),
            ),
        )

        item_provisao = next(iter(table))
        print(item_provisao)
        btn_editar_risco.click()
