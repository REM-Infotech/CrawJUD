# task_manager/bots/intimacoes/projudi/__init__.py

## Propósito

Module: Intimações.

Extract and manage process intimation information from the Projudi system.

## Dependências Principais

- `backend.common.exceptions`
- `backend.controllers.projudi`
- `backend.resources.driver.web_element`
- `backend.resources.elements`
- `contextlib`
- `selenium.webdriver.common.by`
- `selenium.webdriver.support`
- `selenium.webdriver.support.ui`
- `time`

## Classe: `Intimacoes`

Extract and process intimations in Projudi by navigating pages and extracting data.

This class extends CrawJUD to enter the intimacoes tab, set page sizes,
and retrieve detailed process intimation information.

**Herda de:** `ProjudiBot`

### Métodos

#### `execution()`

Execute the intimation extraction loop and handle pagination.

Iterates through intimation pages and queues extraction of process data.

**Parâmetros:**

- `self` (Any)

#### `enter_intimacoes()`

Enter the 'intimações' tab in the Projudi system via script execution.

**Parâmetros:**

- `self` (Any)

#### `aba_initmacoes()`

Retrieve the intimações table element for data extraction.

Returns:
    WebElement: The intimações table element.

**Parâmetros:**

- `self` (Any)

**Retorna:** WebElement

#### `set_page_size()`

Set the page size for the intimacoes table to 100.

**Parâmetros:**

- `self` (Any)

#### `calculate_pages()`

Calculate the total number of intimation pages using table info.

Args:
    aba_intimacoes (WebElement): The intimacoes table element.

Returns:
    int: The total number of pages.

**Parâmetros:**

- `self` (Any)
- `aba_intimacoes` (WebElement)

**Retorna:** int

#### `queue()`

Handle the intimation extraction queue and advance pagination.

Raises:
    ExecutionError: If extraction or navigation fails.

**Parâmetros:**

- `self` (Any)

#### `get_intimacao_information()`

Extract detailed intimation information from table rows.

Args:
    name_colunas (list[WebElement]): Table header elements.
    intimacoes (list[WebElement]): Table row elements for intimations.

Returns:
    dict: Processed intimation data.

**Parâmetros:**

- `self` (Any)
- `name_colunas` (list[WebElement])
- `intimacoes` (list[WebElement])

**Retorna:** dict

#### `get_intimacoes()`

Retrieve the header and row elements from the intimações table.

Args:
    aba_intimacoes (WebElement): The intimacoes table element.

Returns:
    tuple: A tuple containing headers and row elements.

**Parâmetros:**

- `self` (Any)
- `aba_intimacoes` (WebElement)

**Retorna:** tuple[list[WebElement], list[WebElement]]

