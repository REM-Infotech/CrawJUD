from __future__ import annotations

from time import sleep
from typing import TYPE_CHECKING, Literal

from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import presence_of_all_elements_located

from backend.common.exceptions import ExecutionError
from backend.controllers import ElawBot
from backend.resources.auth.jusds import presence_of_element_located
from backend.resources.elements.elaw import ElawCadastroElements as El

if TYPE_CHECKING:
    from backend.dicionarios import ElawCadastro


type SeletoresObrigatorios = list[
    Literal[
        "AREA_DIREITO",
        "SUBAREA_DIREITO",
        "ESFERA",
        "ESTADO",
        "COMARCA",
        "FORO",
        "VARA",
        "EMPRESA",
        "POLO_EMPRESA",
        "POLO_PARTE_CONTRARIA",
        "LOCALIZACAO_PROCESSO",
        "TIPO_ACAO",
        "ESCRITORIO_EXTERNO",
        "CONTIGENCIAMENTO",
    ]
]
CAMPOS_OBRIGATORIOS = [
    "NUMERO_PROCESSO",
    "DOCUMENTO_PARTE",
    "DATA_DISTRIBUICAO",
    "ADVOGADO_CONTRARIO",
    "VALOR_CAUSA",
]


SELETORES_OBRIGATORIOS: SeletoresObrigatorios = [
    "AREA_DIREITO",
    "SUBAREA_DIREITO",
]

ENDERECOS_CAMPOS = {
    "NUMERO_PROCESSO": El.XPATH_INPUT_NUMERO_PROCESSO,
    "DOCUMENTO_PARTE": El.XPATH_INPUT_DOC_PARTE_CONTRARIA,
    "ADVOGADO_CONTRA": El.XPATH_INPUT_ADVOGADO_CONTRARIO,
    "VALOR_CAUSA": El.XPATH_INPUT_VALOR_CAUSA,
    "DATA_DISTRIBUICAO": El.XPATH_INPUT_DATA_DISTRIBUICAO,
}

ENDERECOS_SELETORES = {
    "AREA_DIREITO": El.XPATH_SELECT_AREA_DIREITO,
    "SUBAREA_DIREITO": El.XPATH_SELECT_SUBAREA_DIREITO,
}

INDICES_SELETORES = {
    "ESFERA": 0,
    "ESTADO": 1,
    "COMARCA": 2,
    "FORO": 3,
    "VARA": 4,
    "EMPRESA": 5,
    "POLO_EMPRESA": 6,
    "POLO_PARTE_CONTRARIA": 8,
    "LOCALIZACAO_PROCESSO": 9,
    "TIPO_ACAO": 13,
    "ESCRITORIO_EXTERNO": 21,
    "CONTIGENCIAMENTO": 28,
}


class CadastroElaw(ElawBot):
    bot_data: ElawCadastro

    def cadastrar(self) -> None:

        try:
            for seletor in SELETORES_OBRIGATORIOS:
                text = self.bot_data[seletor]
                xpath_el = ENDERECOS_SELETORES[seletor]
                self.seleciona_item_seletor(text, xpath_el)

                if seletor == "SUBAREA_DIREITO":
                    sleep(2)
                    btn_continuar = self.wait.until(
                        presence_of_element_located((By.XPATH, El.XPATH_BTN_CONTINUAR)),
                    )

                    btn_continuar.click()
                    sleep(2)

            method = presence_of_all_elements_located((
                By.XPATH,
                'select[contains(@id, "_input")]',
            ))
            list_seletores = self.wait.until(method)[3:]
            for key, idx_seletor in list(INDICES_SELETORES.items()):
                text = self.bot_data[key]
                seletor = list_seletores[idx_seletor]
                seletor.select2(text)
                self.sleep_load()

        except Exception as e:
            msg = "Erro ao executar operação!"
            raise ExecutionError(message=msg, exc=e) from e

    def seleciona_item_seletor(self, text: str, xpath_element: str) -> None:

        seletor = self.wait.until(
            presence_of_element_located((By.XPATH, xpath_element)),
        )

        self.select2(seletor, text)
        self.sleep_load()
