# task_manager/bots/buscadores/pagamentos/esaj/__init__.py

## Propósito

Module: busca_pags.

This module manages page search operations for paid costs in the CrawJUD-Bots app.

## Dependências Principais

- `__future__`
- `backend.common.exceptions`
- `backend.controllers.esaj`
- `backend.resources.elements`
- `contextlib`
- `datetime`
- `selenium.webdriver.common.by`
- `selenium.webdriver.remote.webelement`
- `selenium.webdriver.support`
- `typing`

## Classe: `BuscaPags`

Class BuscaPags.

Manages page search and the extraction of cost-related information.

Attributes:
    datetimeNOW (str): The current datetime in "America/Manaus" timezone.


Methods:
    initialize: Create a new BuscaPags instance.
    execution: Run the page search loop.
    queue: Retrieve and process the paid costs page.
    get_page_custas_pagas: Navigate to the paid costs page.
    page_custas: Extract cost details from the paid costs table.

**Herda de:** `ESajBot`

### Métodos

#### `execution()`

Execute page search.

Iterates over each data row, checks session status, and logs errors.

# Inline: For each row, execute the queue sequence.

**Parâmetros:**

- `self` (Any)

#### `queue()`

Queue page search tasks.

Retrieves the paid costs page and processes cost data.

Raises:
    ExecutionError: Propagates errors encountered during page search.

**Parâmetros:**

- `self` (Any)

#### `get_page_custas_pagas()`

Retrieve the paid costs page.

Extracts the URL from the element and navigates to it.

# Inline: Use Selenium to get the onclick attribute and redirect.

**Parâmetros:**

- `self` (Any)

#### `page_custas()`

Process the paid costs page.

Extract cost details from tables and append success records.

**Parâmetros:**

- `self` (Any)

