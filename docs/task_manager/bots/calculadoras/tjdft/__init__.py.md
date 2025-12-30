# task_manager/bots/calculadoras/tjdft/__init__.py

## Propósito

Module: tjdft.

This module handles calculations related to the TJD-Federal Tribunal within the CrawJUD-Bots application.

## Dependências Principais

- `backend.common.exceptions`
- `backend.controllers.head`
- `base64`
- `contextlib`
- `pathlib`
- `selenium.common.exceptions`
- `selenium.webdriver.support`
- `selenium.webdriver.support.ui`
- `selenium.webdriver.support.wait`
- `time`

## Classe: `Tjdft`

The Tjdft class extends CrawJUD to handle calculations for the TJD-Federal Tribunal.

Attributes:
    cookieaceito (list): list to track accepted cookies.

**Herda de:** `CrawJUD`

### Métodos

#### `execution()`

Execute the main processing loop for calculations.

Iterates over each entry in the data frame and processes it.
Handles session expiration and error logger.

**Parâmetros:**

- `self` (Any)

#### `queue()`

Handle the calculation queue processing.

Performs the calculation steps and finalizes the execution.

Raises:
    ExecutionError: If an error occurs during queue processing.

**Parâmetros:**

- `self` (Any)

#### `get_calcular()`

Access the calculation page.

This method navigates to the calculation URL and handles cookie acceptance if prompted.

Raises:
    ExecutionError: If an error occurs while accessing the calculation page.

**Parâmetros:**

- `self` (Any)

#### `info_numproc()`

Inform the process number.

This method fills in the process number in the calculation form.

Raises:
    ExecutionError: If an error occurs while informing the process number.

**Parâmetros:**

- `self` (Any)

#### `info_requerente()`

Inform the petitioner.

This method fills in the petitioner's name in the calculation form.

Raises:
    ExecutionError: If an error occurs while informing the petitioner.

**Parâmetros:**

- `self` (Any)

#### `info_requerido()`

Inform the required party.

This method fills in the required party's name in the calculation form.

Raises:
    ExecutionError: If an error occurs while informing the required party.

**Parâmetros:**

- `self` (Any)

#### `info_jurosapartir()`

Inform the interest starting point.

This method selects the interest starting point in the calculation form and informs the associated data.

Raises:
    ExecutionError: If an error occurs while informing the interest starting point.

**Parâmetros:**

- `self` (Any)

#### `valores_devidos()`

Inform the owed values.

This method fills in the owed values and their dates in the calculation form.

Raises:
    ExecutionError: If an error occurs while informing the owed values.

**Parâmetros:**

- `self` (Any)

#### `acessorios()`

Inform accessory values like penalties and fees.

This method handles the input of accessory financial details in the calculation form.

**Parâmetros:**

- `self` (Any)

#### `finalizar_execucao()`

Finalize the execution of the calculation.

This method submits the calculation form, retrieves the calculated value, and saves the PDF receipt.

Raises:
    ExecutionError: If an error occurs during finalization.

**Parâmetros:**

- `self` (Any)

#### `multa_percentual()`

Informe multa percentual e valores relacionados.

Preencha os campos de multa percentual e valores associados no formulário.

Raises:
    ExecutionError: Se ocorrer erro ao informar multa percentual.

**Parâmetros:**

- `self` (Any)

#### `honorario_sucumb()`

Informe honorários de sucumbência.

Preencha os campos de honorários de sucumbência no formulário.

Raises:
    ExecutionError: Se ocorrer erro ao informar honorários de sucumbência.

**Parâmetros:**

- `self` (Any)

#### `percent_multa_475j()`

Informe percentual da multa 475J.

Preencha o campo de percentual da multa 475J no formulário.

Raises:
    ExecutionError: Se ocorrer erro ao informar percentual da multa 475J.

**Parâmetros:**

- `self` (Any)

#### `honorario_cumprimento()`

Informe honorários de cumprimento.

Preencha os campos de honorários de cumprimento no formulário.

Raises:
    ExecutionError: Se ocorrer erro ao informar honorários de cumprimento.

**Parâmetros:**

- `self` (Any)

#### `custas()`

Informe valores de custas processuais.

Preencha os campos de custas processuais no formulário.

Raises:
    ExecutionError: Se ocorrer erro ao informar custas processuais.

**Parâmetros:**

- `self` (Any)

