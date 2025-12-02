"""Update ElawAme module docstring to Google style.

This module provides selectors for automating ELAW operations.
"""

from typing import ClassVar

LINK_PROCESSO_LIST = "https://amazonas.elaw.com.br/processoList.elaw"


class SolicitaPagamento:
    """Defina seletores e tipos para solicitações de pagamento ELAW."""

    CSS_LOAD = 'div[id="j_id_3p"]'
    TIPOS_PAGAMENTOS: ClassVar[dict[str, str]] = {
        "Acordo": "109",
        "Condenação": "111",
        "Custas": "102",
        "Honorários Advocatícios": "110",
        "Pagamento Voluntário": "232",
        "Pagamento de Seguro Fiança": "213",
    }

    CSS_BTN_NOVO_PGTO = (
        'button[id="tabViewProcesso:pvp-pgBotoesValoresPagamentoBtnNovo"]'
    )

    XPATH_TIPO_PAGAMENTO = '//select[@id="processoValorPagamentoEditForm:pvp:processoValorPagamentoTipoCombo_input"]'
    XPATH_BTN_TELA_PGTO = '//a[@href="#tabViewProcesso:processoValorPagamento"]'
    CSS_MODAL_LOAD_PROCESSOVIEW = 'div[id="j_id_hh"]'

    XPATH_INPUT_UPLOAD_FILE = '//input[contains(@id, "processoValorPagamentoEditForm") and contains(@id, "uploadGedEFile_input")]'
    XPATH_SELECT_TIPO_ARQUIVO = '//select[contains(@id, "processoValorPagamentoEditForm:pvp") and contains(@id, ":eFileTipoCombo")]'

    XPATH_SELECTS_INFORMACOES = '//select[contains(@id, "processoValorPagamentoEditForm:pvp") and contains(@name, "pvpEFBtypeSelectField1CombosCombo_input")]'

    XPATH_DESCRICAO_PGTO = '//textarea[@id="processoValorPagamentoEditForm:pvp:processoValorPagamentoDescription"]'
    XPATH_DATA_VENCIMENTO = '//input[@id="processoValorPagamentoEditForm:pvp:processoValorPagamentoVencData_input"]'
    XPATH_INPUT_FAVORECIDO = '//input[@id="processoValorPagamentoEditForm:pvp:processoValorFavorecido_input"]'
    XPATH_INFO_FAVORECIDO = '//span[@id="processoValorPagamentoEditForm:pvp:processoValorFavorecido_panel"]'
    XPATH_SELECT_FORMA_PGTO = (
        '//select[contains(@id, "pvpEFSpgTypeSelectField1CombosCombo")]'
    )
    XPATH_INPUT_CODIGO_BARRAS = '//input[contains(@id, "processoValorPagamentoEditForm:pvp:") and contains(@maxlength, "4000") and not(contains(@id, "pvpEFBfieldText"))]'
    XPATH_INPUT_CENTRO_CUSTA = '//input[contains(@id, "processoValorPagamentoEditForm:pvp") and contains(@id, "pvpEFBfieldText")]'
    XPATH_BTN_SALVAR = '//input[@id="processoValorPagamentoEditForm:btnSalvarProcessoValorPagamento"]'

    XPATH_TBODY_PAGAMENTOS = (
        '//tbody[@id="tabViewProcesso:pvp-dtProcessoValorResults_data"]'
    )

    XPATH_BTN_VER_PGTO = (
        '//button[contains(@id, "pvp-pgBotoesValoresPagamentoBtnVer")]'
    )

    XPATH_MODAL_PAGAMENTO_INFO = '//div[contains(@id, "tabViewProcesso:pvp-dtProcessoValorResults:{pos}:") and contains(@id, "pvp-pgBotoesValoresPagamentoBtnVer_dlg") and not(contains(@id, "_modal"))]'
    XPATH_CODIGO_BARRAS = '//div[text()="{codigo_barra}"]'
    XPATH_BTN_FECHAR = '//button[@id="j_id_v"]'
    XPATH_MODAL_PAGAMENTO_DIALOG = '//div[@id="tabViewProcesso:pvp-dtProcessoValorResults:{pos}:pvp-pgBotoesValoresPagamentoBtnVer_dlg_modal"]'


class PgtoCondenacao(SolicitaPagamento):
    """Defina seletores para pagamentos de condenação no ELAW."""

    CSS_UPLOAD_FILE_PROGRESS_BAR = 'div[class="ui-fileupload-row"]'
    XPATH_INPUT_VALOR_CONDENACAO = '//input[contains(@id, ":processoValorRateioAmountAllDt") and contains(@id, "_input")]'


class PgtoCustas(SolicitaPagamento):
    """Defina seletores para pagamentos de custas no ELAW."""

    XPATH_INPUT_VALOR = (
        '//input[@id="processoValorPagamentoEditForm:pvp:valorField_input"]'
    )


class AtualizaFase:
    """Defina seletores para atualizar fases no ELAW."""

    XPATH_BTN_ALTERAR_FASE = '//button[@id="btnTrocarFase"]'
    XPATH_FORM_ALTERA_FASE = '//form[@id="trocarFaseForm"]'
    XPATH_SELETOR_FASE = '//select[@id="comboFase_input"]'
    XPATH_BTN_SALVAR = '//button[@id="btnTrocarFaseSalvar"]'
    XPATH_CONTAINER_ALTERA_FASE = '//div[@id="comboFase"]'
    XPATH_FORM_INFORMACAO_PROCESSO = (
        '//form[@id="processoDadosCabecalhoForm"][@action="/processoView.elaw"]'
    )

    XPATH_TEXTO_FASE = '//form[@id="processoDadosCabecalhoForm"][@action="/processoView.elaw"]/table/tbody/tr[3]/td[6]/label'
