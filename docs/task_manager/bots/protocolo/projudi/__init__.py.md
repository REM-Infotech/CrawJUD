# task_manager/bots/protocolo/projudi/__init__.py

## Propósito

Módulo de protocolo do bot Projudi.

Automatiza o protocolo de processos no sistema Projudi.

## Dependências Principais

- `backend.common`
- `backend.common.exceptions`
- `backend.controllers.projudi`
- `backend.resources.elements`
- `backend.resources.formatadores`
- `contextlib`
- `selenium.webdriver`
- `selenium.webdriver.common.by`
- `selenium.webdriver.support`
- `selenium.webdriver.support.ui`

## Classe: `Protocolo`

Executa o protocolo de processos no Projudi.

Herda de ProjudiBot e implementa a lógica de protocolo.

**Herda de:** `ProjudiBot`

### Métodos

#### `execution()`

Execute o protocolo dos processos no Projudi.

**Parâmetros:**

- `self` (Any)

#### `queue()`

Realize o protocolo de um processo no Projudi.

**Parâmetros:**

- `self` (Any)

#### `__entra_pagina_protocolo()`

**Parâmetros:**

- `self` (Any)

#### `__informa_tipo_protocolo()`

**Parâmetros:**

- `self` (Any)

#### `__seleciona_parte_interessada()`

**Parâmetros:**

- `self` (Any)

#### `__adicionar_arquivos()`

**Parâmetros:**

- `self` (Any)

#### `__check_contains_files()`

**Parâmetros:**

- `self` (Any)

#### `__peticao_principal()`

**Parâmetros:**

- `self` (Any)

#### `__anexos_adicionais()`

**Parâmetros:**

- `self` (Any)

#### `__envia_arquivo()`

Realiza o envio de um arquivo para o sistema Projudi e seleciona seu tipo.

Args:
    nome_arquivo (str): Nome do arquivo a ser enviado.
    tipo_arquivo (str): Tipo do arquivo a ser selecionado.
    peticao_principal (bool): Indica se é petição principal.

Raises:
    FileError: Caso o arquivo não seja encontrado após upload.

**Parâmetros:**

- `self` (Any)
- `nome_arquivo` (str)
- `tipo_arquivo` (str)

#### `__seleciona_tipo_arquivo()`

**Parâmetros:**

- `self` (Any)
- `tr_arquivo` (WebElement)
- `tipo_arquivo` (str)

#### `__assinar()`

**Parâmetros:**

- `self` (Any)

#### `__confirma_protocolo()`

**Parâmetros:**

- `self` (Any)

**Retorna:** str | None

#### `__finaliza_peticionamento()`

**Parâmetros:**

- `self` (Any)

#### `__screenshot_sucesso()`

Capture and merge screenshots after successful protocol processing.

Returns:
    DataSucesso: DataSucesso

**Parâmetros:**

- `self` (Any)

**Retorna:** DataSucesso

#### `__wait_upload_file()`

**Parâmetros:**

- `self` (Any)

#### `__confirma_inclusao()`

**Parâmetros:**

- `self` (Any)

