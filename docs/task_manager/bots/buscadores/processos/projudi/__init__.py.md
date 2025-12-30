# task_manager/bots/buscadores/processos/projudi/__init__.py

## Propósito

Module: proc_parte.

Manage participant processing in the Projudi system by interacting with process lists and varas.

## Dependências Principais

- `backend.common.exceptions`
- `backend.controllers.projudi`
- `backend.resources.driver.web_element`
- `backend.resources.elements`
- `contextlib`
- `pathlib`
- `selenium.common.exceptions`
- `selenium.webdriver.common.by`

## Classe: `ProcParte`

Handle participant processing in Projudi with detailed queue management and error handling.

This class extends CrawJUD to retrieve process lists, store participant information,
and manage queue execution for the Projudi system.

**Herda de:** `ProjudiBot`

### Métodos

#### `execution()`

Execute the main loop for participant processing continuously.

Continuously process queues until stopping, while handling session expirations and errors.

**Parâmetros:**

- `self` (Any)

#### `queue()`

Manage the participant processing queue and handle varas search.

**Parâmetros:**

- `self` (Any)

#### `get_process_list()`

Retrieve and process the list of processes from the web interface.

Extracts process data, manages pagination, and stores the retrieved information.

Raises:
    ExecutionError: Erro de execução

**Parâmetros:**

- `self` (Any)

#### `use_list_process()`

Extract and log details from each process element in the provided list.

Args:
    list_processos (list[WebElement]): List of process web elements.

**Parâmetros:**

- `self` (Any)
- `list_processos` (list[WebElement])

