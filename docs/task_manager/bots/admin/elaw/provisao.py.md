# task_manager/bots/admin/elaw/provisao.py

## Propósito

Automatize operações de provisão no sistema ELAW.

Este módulo contém a classe Provisao e funções auxiliares
para gerenciar e atualizar provisões de processos via Selenium.

## Dependências Principais

- `__future__`
- `backend.controllers.elaw`
- `backend.resources.elements`
- `contextlib`
- `datetime`
- `selenium.common.exceptions`
- `selenium.webdriver`
- `selenium.webdriver.support`
- `time`
- `typing`

## Classe: `Provisao`

Gerencie e atualize provisões de processos no ELAW.

Esta classe automatiza operações de provisão usando Selenium.

**Herda de:** `ElawBot`

### Métodos

#### `execution()`

Execute a automação das provisões para todos os processos.

**Parâmetros:**

- `self` (Any)

#### `queue()`

Execute a fila de operações de provisão para um processo.

Executa as etapas necessárias para atualizar a provisão de um processo.

**Parâmetros:**

- `self` (Any)

#### `verifica_classe_risco()`

Verifique e ajuste a classificação de risco se necessário.

Ajusta o campo de risco para "Risco" caso esteja "Risco Quebrado".

**Parâmetros:**

- `self` (Any)

#### `setup_calls()`

Defina e retorne a lista de funções para atualizar provisão.

Returns:
    list: Lista de funções a serem executadas na atualização.

**Parâmetros:**

- `self` (Any)

**Retorna:** list

#### `get_valores_proc()`

Verifique e retorne o status dos valores da provisão.

Returns:
    str: Status dos valores encontrados na provisão.

**Parâmetros:**

- `self` (Any)

**Retorna:** str

#### `adiciona_nova_provisao()`

Adicione nova provisão ao processo no sistema ELAW.

Raises:
    ExecutionError: Caso não seja possível atualizar provisão.

**Parâmetros:**

- `self` (Any)

#### `edita_provisao()`

Edite a provisão do processo no sistema ELAW.

**Parâmetros:**

- `self` (Any)

#### `atualiza_valores()`

Atualize os valores da provisão no sistema ELAW.

**Parâmetros:**

- `self` (Any)

#### `atualiza_risco()`

Atualize o risco da provisão conforme o valor informado.

Atualiza o campo de risco na tabela de valores do processo.

**Parâmetros:**

- `self` (Any)

#### `informar_datas()`

Atualize datas de correção base e juros da provisão.

**Parâmetros:**

- `self` (Any)

#### `informa_justificativa()`

Informe a justificativa da atualização da provisão.

**Parâmetros:**

- `self` (Any)

#### `save_changes()`

Salve as alterações realizadas na provisão do processo.

Raises:
    ExecutionError: Caso não seja possível atualizar provisão.

**Parâmetros:**

- `self` (Any)

#### `set_data_correcao()`

Atualize a data base de correção da provisão no ELAW.

**Parâmetros:**

- `self` (Any)
- `data_base_correcao` (str)

#### `set_data_juros()`

Atualize a data base de juros da provisão no ELAW.

**Parâmetros:**

- `self` (Any)
- `data_base_juros` (str)

#### `__tabela_valores()`

**Parâmetros:**

- `self` (Any)

**Retorna:** list[WebElement]

