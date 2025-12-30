# task_manager/bots/protocolo/esaj/__init__.py

## Propósito

Gerencie operações de protocolo no sistema ESaj via CrawJUD.

Este pacote contém classes e funções para automação do
peticionamento eletrônico no ESaj.

## Dependências Principais

- `__future__`
- `backend.common.raises`
- `backend.controllers.esaj`
- `backend.resources.driver`
- `contextlib`
- `pathlib`
- `selenium.common.exceptions`
- `selenium.webdriver.support`
- `typing`
- `unicodedata`

## Classe: `Protocolo`

Class Protocolo.

Manage protocol operations in the ESaj system via CrawJUD.

Attributes:
    start_time (float): Time when the protocol process starts.
    bot_data (dict): Data for the current protocol entry.


Methods:
    initialize: Create and return a new Protocolo instance.
    execution: Run protocol processing loop.
    queue: Execute protocoling steps with error handling.
    init_protocolo: Start the petition process.
    set_tipo_protocolo: Select and input the protocol type.
    set_subtipo_protocolo: Select and input the protocol subtype.
    set_petition_file: Attach the petition document.
    vincular_parte: Link a party to the petition.
    finish_petition: Finalize petition process.
    get_confirm_protocol: Confirm protocol and process receipt.

**Herda de:** `ESajBot`

### Métodos

#### `execution()`

Execute protocol processing on each row.

Iterates over protocol rows and handles session renewals and errors.

**Parâmetros:**

- `self` (Any)

#### `queue()`

Execute etapas do protocolo com tratamento de erros.

Raises:
    ExecutionError: Caso ocorra erro em alguma etapa.

**Parâmetros:**

- `self` (Any)

#### `init_protocolo()`

Inicie o peticionamento no sistema ESaj.

Raises:
    ExecutionError: Caso ocorra erro ao inicializar peticionamento.

**Parâmetros:**

- `self` (Any)

#### `set_tipo_protocolo()`

Informe o tipo de protocolo no sistema ESaj.

Raises:
    ExecutionError: Caso ocorra erro ao informar o tipo.

**Parâmetros:**

- `self` (Any)

#### `set_subtipo_protocolo()`

Informe o subtipo de protocolo no sistema ESaj.

Raises:
    ExecutionError: Caso ocorra erro ao informar o subtipo.

**Parâmetros:**

- `self` (Any)

#### `set_petition_file()`

Attach petition file.

Uploads the petition document and verifies its successful submission.

Raises:
    ExecutionError: If the petition file fails to upload.

**Parâmetros:**

- `self` (Any)

#### `vincular_parte()`

Vincule a parte à petição conforme os dados do bot.

Raises:
    ExecutionError: Caso não seja possível vincular a parte.

**Parâmetros:**

- `self` (Any)

#### `_vincular_parte_peticao()`

Auxilia na vinculação da parte à petição.

Args:
    partes (list): Lista de elementos de partes.
    parte_peticao (str): Nome da parte a ser vinculada.

**Parâmetros:**

- `self` (Any)
- `partes` (list[WebElement])
- `parte_peticao` (str)

#### `finish_petition()`

Finalize petition process.

Completes the petition process by confirming and saving process details.

# Inline: Click finish and then confirm the petition.

**Parâmetros:**

- `self` (Any)

#### `get_confirm_protocol()`

Confirma protocolo e obtenha informações do recibo.

Returns:
    list: Lista com número do processo, mensagem e nome do recibo.

Raises:
    ExecutionError: Caso ocorra erro ao confirmar protocolo.

**Parâmetros:**

- `self` (Any)

**Retorna:** list

