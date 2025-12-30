# task_manager/bots/emissao/esaj/__init__.py

## Propósito

Implemente emissão de guias judiciais via ESAJ.

Este pacote automatiza a geração e download de guias judiciais.

## Dependências Principais

- `backend.common.raises`
- `backend.controllers.esaj`
- `backend.resources.elements`
- `contextlib`
- `pathlib`
- `pypdf`
- `requests`
- `selenium.common.exceptions`
- `selenium.webdriver.support`
- `selenium.webdriver.support.wait`

## Classe: `Emissao`

Emissão de guias Esaj.

**Herda de:** `ESajBot`

### Métodos

#### `execution()`

Execute o fluxo principal de emissão de guias ESaj.

**Parâmetros:**

- `self` (Any)

#### `queue()`

Queue emission tasks by generating docs and processing PDF barcodes.

Executes the emission process by calling the appropriate method based on
the guide type and then downloading the PDF.

Raises:
    ExecutionError: Erro de execução

**Parâmetros:**

- `self` (Any)

#### `custas_iniciais()`

Realize emissão de guia de custas iniciais no ESAJ.

Esta função preenche os campos necessários para gerar a guia
de custas iniciais no portal ESAJ, utilizando os dados da linha
atual da planilha.

**Parâmetros:**

- `self` (Any)

#### `preparo_ri()`

Realize emissão de guia de preparo RI conforme o portal.

**Parâmetros:**

- `self` (Any)

#### `generate_doc()`

Gere e retorne a URL do PDF da guia emitida pelo ESAJ.

Returns:
    str: URL do PDF gerado pelo ESAJ.

**Parâmetros:**

- `self` (Any)

**Retorna:** str

#### `downloadpdf()`

Baixe o PDF da guia emitida pelo ESAJ.

**Parâmetros:**

- `self` (Any)
- `link_pdf` (str)

#### `get_barcode()`

Extraia o código de barras do PDF gerado pela emissão da guia.

Raises:
    ExecutionError: Erro ao extrair o código de barras.

**Parâmetros:**

- `self` (Any)

