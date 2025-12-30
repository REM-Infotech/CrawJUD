# task_manager/bots/admin/elaw/andamentos.py

## Propósito

Robô de automação elaw andamentos.

## Dependências Principais

- `backend.common.exceptions`
- `backend.controllers.elaw`
- `backend.resources.elements`
- `selenium.webdriver`
- `selenium.webdriver.common.by`
- `selenium.webdriver.support`
- `selenium.webdriver.support.wait`
- `time`

## Classe: `Andamentos`

Gerencie e execute o fluxo de andamentos no sistema Elaw.

Métodos:
    execution(): Execute o processamento principal.
    queue(): Processe a fila de andamentos.
    info_data(): Informe a data do andamento.
    info_ocorrencia(): Informe a ocorrência do andamento.
    info_observacao(): Informe a observação do andamento.
    add_anexo(): Adicione anexos ao andamento.
    save_andamento(): Salve os dados do andamento.

**Herda de:** `ElawBot`

### Métodos

#### `execution()`

Execute the main processing loop for andamentos.

Iterates over each entry in the data frame and processes it.
Handles session expiration and error logger.

**Parâmetros:**

- `self` (Any)

#### `queue()`

Processa a fila de andamentos do Elaw.

Executa busca, preenche dados e trata anexos e erros.

**Parâmetros:**

- `self` (Any)

#### `info_data()`

Inform the date of the andamento.

This method fills in the date field in the andamento form.

Raises:
    ExecutionError: If an error occurs while informing the date.

**Parâmetros:**

- `self` (Any)

#### `info_ocorrencia()`

Inform the occurrence details of the andamento.

This method fills in the occurrence details in the andamento form.

Raises:
    ExecutionError: If an error occurs while informing the occurrence.

**Parâmetros:**

- `self` (Any)

#### `info_observacao()`

Inform the observation details of the andamento.

This method fills in the observation details in the andamento form.

Raises:
    ExecutionError: If an error occurs while informing the observation.

**Parâmetros:**

- `self` (Any)

#### `add_anexo()`

Add attachments to the andamento.

This method handles the addition of attachments to the andamento form.

Raises:
    NotImplementedError: If the method is not yet implemented.

**Parâmetros:**

- `self` (Any)

#### `save_andamento()`

Salve o andamento no sistema Elaw.

Raises:
    ExecutionError: Caso não seja possível salvar o andamento.

**Parâmetros:**

- `self` (Any)

