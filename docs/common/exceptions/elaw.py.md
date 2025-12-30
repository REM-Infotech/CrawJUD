# common/exceptions/elaw.py

## Propósito

Módulo de exceptions elaw.

## Dependências Principais

- `__future__`
- `backend.common.exceptions`
- `logging`
- `traceback`

## Classe: `ElawError`

Exception genérico de erros Elaw.

**Herda de:** `BaseCrawJUDError`

### Métodos

#### `__init__()`

Exception para erros de salvamento de Formulários/Arquivos.

**Parâmetros:**

- `self` (Any)
- `exception` (Exception)
- `bot_execution_id` (str)
- `message` (str)

#### `__str__()`

Retorne a representação em string da exceção.

Returns:
    str: Representação textual da mensagem de erro.

**Parâmetros:**

- `self` (Any)

**Retorna:** str

## Classe: `AdvogadoError`

Exception para erros de Inserção/Cadastro de advogado no elaw.

**Herda de:** `BaseCrawJUDError`

### Métodos

#### `__init__()`

Exception para erros de salvamento de Formulários/Arquivos.

**Parâmetros:**

- `self` (Any)
- `bot_execution_id` (str)
- `exception` (Exception | None)
- `message` (str)

#### `__str__()`

Retorne a representação em string da exceção.

Returns:
    str: Representação textual da mensagem de erro.

**Parâmetros:**

- `self` (Any)

**Retorna:** str

