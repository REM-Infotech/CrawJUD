# interfaces/__init__.py

## Propósito

Módulo de interfaces do task manager.

## Dependências Principais

- `__future__`
- `backend.types_app`
- `backend.types_app.payloads`
- `typing`

## Classe: `DictUsers`

**Herda de:** `TypedDict`

### Atributos

- `Id` (int)
- `login` (str)
- `nome_usuario` (str)
- `email` (str)
- `password` (str)
- `login_time` (str)
- `verification_code` (str)
- `login_id` (str)
- `filename` (str)
- `blob_doc` (bytes)
- `licenseus_id` (int)

## Classe: `DictCredencial`

**Herda de:** `TypedDict`

### Atributos

- `Id` (8)
- `nome_credencial` (str)
- `system` (SystemBots)
- `login_metodo` (str)
- `login` (str)
- `password` (str)

## Classe: `DataSave`

Estrutura para salvar dados do bot em planilhas do sistema.

Args:
    worksheet (str): Nome da planilha onde os dados serão salvos.
    data_save (list[BotData]): Lista de dados do bot a serem
        armazenados.

Returns:
    TypedDict: Estrutura contendo nome da planilha e dados do bot.

Raises:
    KeyError: Se uma das chaves obrigatórias estiver ausente.

**Herda de:** `TypedDict`

### Atributos

- `worksheet` (str)
- `data_save` (list[BotData])

## Classe: `Message`

Defina estrutura para mensagens do bot.

**Herda de:** `TypedDict`

### Atributos

- `pid` (str)
- `message` (str)
- `time_message` (str)
- `message_type` (MessageType)
- `status` (StatusBot)
- `start_time` (str)
- `row` (int)
- `total` (int)
- `erros` (int)
- `sucessos` (int)
- `restantes` (int)
- `link` (str)

## Classe: `ColorsDict`

Dicionário de cores para mensagens do bot, conforme o padrão.

Args:
    info (Literal["cyan"]): Cor para mensagens informativas.
    log (Literal["yellow"]): Cor para mensagens de log.
    error (Literal["red"]): Cor para mensagens de erro.
    warning (Literal["magenta"]): Cor para mensagens de aviso.
    success (Literal["green"]): Cor para mensagens de sucesso.

Returns:
    TypedDict: Estrutura contendo os tipos de cores para cada
        mensagem.

Raises:
    KeyError: Se uma das chaves obrigatórias estiver ausente.

**Herda de:** `TypedDict`

### Atributos

- `info` (Literal['cyan'])
- `log` (Literal['yellow'])
- `error` (Literal['red'])
- `warning` (Literal['magenta'])
- `success` (Literal['green'])

## Classe: `DataSucesso`

Defina estrutura para dados de sucesso do bot.

Args:
    NUMERO_PROCESSO (str): Número do processo.
    MENSAGEM (str): Mensagem de sucesso.
    NOME_COMPROVANTE (str): Nome do comprovante.
    NOME_COMPROVANTE_2 (str): Nome do segundo comprovante.

**Herda de:** `TypedDict`

### Atributos

- `NUMERO_PROCESSO` (str)
- `MENSAGEM` (str)
- `NOME_COMPROVANTE` (str)
- `NOME_COMPROVANTE_2` (str)

## Classe: `BotData`

TypedDict for bot data.

**Herda de:** `TypedDict`

### Atributos

- `NUMERO_PROCESSO` (str)
- `GRAU` (int | str)
- `POLO_PARTE` (PolosProcessuais)
- `FORO` (str)
- `VALOR_CALCULADO` (str)
- `ADVOGADO_INTERNO` (str)
- `TIPO_EMPRESA` (str)
- `VARA` (str)
- `COMARCA` (str)
- `TIPO_GUIA` (str)
- `VALOR_CAUSA` (str)
- `TRIBUNAL` (str)
- `AGENCIA` (str)
- `TIPO_ACAO` (str)
- `AUTOR` (str)
- `CPF_CNPJ_AUTOR` (str)
- `REU` (str)
- `CPF_CNPJ_REU` (str)
- `NOME_CUSTOM` (str)
- `TEXTO_DESC` (str)
- `DATA_PGTO` (str)
- `VIA_CONDENACAO` (str)
- `REQUERENTE` (str)
- `REQUERIDO` (str)
- `JUROS_PARTIR` (str)
- `JUROS_PERCENT` (str)
- `DATA_INCIDENCIA` (str)
- `DATA_CALCULO` (str)
- `MULTA_PERCENTUAL` (str)
- `MULTA_DATA` (str)
- `HONORARIO_SUCUMB_PERCENT` (str)
- `HONORARIO_SUCUMB_DATA` (str)
- `HONORARIO_SUCUMB_VALOR` (str)
- `HONORARIO_SUCUMB_PARTIR` (str)
- `PERCENT_MULTA_475J` (str)
- `HONORARIO_CUMPRIMENTO_PERCENT` (str)
- `HONORARIO_CUMPRIMENTO_DATA` (str)
- `HONORARIO_CUMPRIMENTO_VALOR` (str)
- `HONORARIO_CUMPRIMENTO_PARTIR` (str)
- `CUSTAS_DATA` (str)
- `CUSTAS_VALOR` (str)
- `ANEXOS` (list[str])
- `DATA` (str)
- `OCORRENCIA` (str)
- `OBSERVACAO` (str)
- `AREA_DIREITO` (str)
- `SUBAREA_DIREITO` (str)
- `ESTADO` (str)
- `EMPRESA` (str)
- `PARTE_CONTRARIA` (str)
- `ADV_PARTE_CONTRARIA` (str)
- `TIPO_PARTE_CONTRARIA` (str)
- `DOC_PARTE_CONTRARIA` (str)
- `CAPITAL_INTERIOR` (str)
- `ACAO` (str)
- `DATA_DISTRIBUICAO` (str)
- `ESCRITORIO_EXTERNO` (str)
- `ESFERA` (str)
- `UNIDADE_CONSUMIDORA` (str)
- `LOCALIDADE` (str)
- `BAIRRO` (str)
- `DIVISAO` (str)
- `DATA_CITACAO` (str)
- `FASE` (str)
- `PROVIMENTO` (str)
- `FATO_GERADOR` (str)
- `DESC_OBJETO` (str)
- `OBJETO` (str)
- `TERMOS` (str)
- `PROVISAO` (str)
- `DATA_BASE_CORRECAO` (str)
- `DATA_BASE_JUROS` (str)
- `VALOR_ATUALIZACAO` (str)
- `OBSERVACAO` (str)
- `TIPO_PAGAMENTO` (str)
- `VALOR_GUIA` (str)
- `DOC_GUIA` (str)
- `DOC_CALCULO` (str)
- `TIPO_CONDENACAO` (str)
- `DESC_PAGAMENTO` (str)
- `DATA_LANCAMENTO` (str)
- `CNPJ_FAVORECIDO` (str)
- `COD_BARRAS` (str)
- `SOLICITANTE` (str)
- `CLASSE` (str)
- `NOME_INTERESSADO` (str)
- `CPF_CNPJ` (str)
- `PORTAL` (str)
- `TRAZER_COPIA` (str)
- `PALAVRAS_CHAVE` (str)
- `DATA_INICIO` (str)
- `DATA_FIM` (str)
- `INTIMADO` (str)
- `DOC_SEPARADOR` (str)
- `TRAZER_TEOR` (str)
- `USE_GPT` (str)
- `TRAZER_PDF` (str)
- `ANEXOS` (str)
- `TIPO_PROTOCOLO` (str)
- `TIPO_ARQUIVO` (str)
- `TIPO_ANEXOS` (str)
- `SUBTIPO_PROTOCOLO` (str)
- `PETICAO_PRINCIPAL` (str)
- `PARTE_PETICIONANTE` (str)
- `TIPO` (str)
- `SUBTIPO` (str)
- `DESCRICAO` (str)
- `ATRIBUIR_PARA` (str)
- `SITUACAO_EXECUCAO` (str)
- `VALOR_MULTA` (str)
- `VALOR_PGTO` (str)
- `DATA_ATUALIZACAO` (str)
- `NUMERO_COMPROMISSO` (str)
- `NUMERO_CHAMADO` (str)

