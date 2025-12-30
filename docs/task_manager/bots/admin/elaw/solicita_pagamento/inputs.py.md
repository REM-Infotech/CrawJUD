# task_manager/bots/admin/elaw/solicita_pagamento/inputs.py

## Propósito

Gerencie o preenchimento de campos para solicitações de pagamento.

Este módulo contém a classe Inputs, responsável por preencher
campos de formulários no sistema de pagamentos automatizados.

## Dependências Principais

- `__future__`
- `backend.resources.driver`
- `backend.resources.elements.elaw`
- `backend.resources.formatadores`
- `contextlib`
- `properties`
- `selenium.webdriver.common.by`
- `selenium.webdriver.support`
- `typing`

## Classe: `Inputs`

Gerencie o preenchimento dos campos de pagamento no sistema.

**Herda de:** `Geral`

### Métodos

#### `informa_valor()`

Preencha o valor da guia de condenação no campo correto.

Args:
    element_input (str): XPath do campo de valor a ser preenchido.

**Parâmetros:**

- `self` (Any)
- `element_input` (str)

#### `informa_descricao()`

Insira a descrição do pagamento no campo apropriado.

Esta função preenche o campo de descrição do pagamento
utilizando o valor presente nos dados do bot.

**Parâmetros:**

- `self` (Any)

#### `informa_data_vencimento()`

Preencha a data de vencimento no campo correspondente.

Esta função insere a data de vencimento do pagamento
conforme os dados fornecidos pelo bot.

**Parâmetros:**

- `self` (Any)

#### `informa_favorecido()`

Informe o CNPJ do favorecido no campo apropriado.

Args:
    cnpj_favorecido (str): CNPJ do favorecido.

**Parâmetros:**

- `self` (Any)
- `cnpj_favorecido` (str)

#### `informa_centro_custa()`

Preencha o centro de custas no campo correspondente.

Args:
    centro_custa (str): Valor do centro de custas.

**Parâmetros:**

- `self` (Any)
- `centro_custa` (str)

#### `upload_files()`

Realize o upload de arquivos para o sistema Elaw.

Args:
    arquivos (list[str]): Lista de nomes dos arquivos.
    tipo_documento (TipoDocumento): Tipo do documento a ser enviado.
    elemento_input_file (str): XPath do campo de upload.

**Parâmetros:**

- `self` (Any)
- `arquivos` (list[str])
- `tipo_documento` (TipoDocumento)

