LINK_PROCESSO_LIST = "https://amazonas.elaw.com.br/processoList.elaw"
XPATH_ELEMENT_LOAD = '//div[contains(@class, "ui-dialog") and contains(@style, "width: 100px")]'
LINK_CADASTRO_PARTE_CONTRA = (
    "https://amazonas.elaw.com.br/includes/processo/cadastro/parteContraria.elaw"
)
LINK_CADASTRO_TERCEIRO = "https://amazonas.elaw.com.br/includes/processo/cadastro/outraParte.elaw"
LINK_CADASTRO_ADVOGADO_CONTRA = (
    "https://amazonas.elaw.com.br/includes/processo/cadastro/lawyerOutraParte.elaw"
)


class ElawCadastroElements:
    CSS_BTN_NOVO_PROCESSO = 'button[id="btnNovo"]'
    XPATH_SELECT_AREA_DIREITO = '//select[@id="comboArea_input"]'
    XPATH_SELECT_SUBAREA_DIREITO = '//select[@id="comboAreaSub_input"]'
    XPATH_BTN_CONTINUAR = '//button[@id="btnContinuar"]'
    XPATH_SELETOR_ESFERA = '//select[contains(@id, "comboRito_input")]'
    XPATH_SELETOR_ESTADO = '//select[contains(@id, "comboEstadoVara_input")]'
    XPATH_SELETOR_COMARCA = '//select[contains(@id, "comboComarcaVara_input")]'
    XPATH_SELETOR_FORO = '//select[contains(@id, "comboForoTribunal_input")]'
    XPATH_SELETOR_VARA = '//select[contains(@id, "comboVara_input")]'

    # Partes
    XPATH_SELETOR_EMPRESA = '//select[contains(@id, "comboClientProcessoParte_input")]'
    XPATH_SELETOR_POLO_EMPRESA = '//select[contains(@id, "comboClientProcessoParte_input")]'

    XPATH_INPUT_NUMERO_PROCESSO = '//input[contains(@id, "txtNumeroMask")]'
    XPATH_INPUT_DOC_PARTE_CONTRARIA = '//input[contains(@id, "autocompleteParteContraria_input")]'
    XPATH_INPUT_ADVOGADO_CONTRARIO = (
        '//input[contains(@id, "autoCompleteLawyerOutraParte_input")]'
    )
    XPATH_INPUT_VALOR_CAUSA = '//input[contains(@id, "amountCase_input")]'
    XPATH_BTN_ADVOGADO_CONTRARIO = '//li[contains(@id, "autoCompleteLawyerOutraParte_item")]'
    XPATH_INPUT_DATA_DISTRIBUICAO = '//input[contains(@id, "dataDistribuicao_input")]'
