# common/exceptions/database.py

## Propósito

Exceções customizadas para operações de banco de dados em módulos internos.

Fornece classes de exceção específicas para erros de exclusão, atualização e
inserção de registros, detalhando o rastreamento de exceções originais.

## Dependências Principais

- `__future__`
- `traceback`

## Classe: `DeleteError`

Exception raised when trying to delete the user itself.

**Herda de:** `Exception`

### Métodos

#### `__init__()`

Initialize the exception.

**Parâmetros:**

- `self` (Any)
- `exc` (Exception | None)
- `message` (str | None)

#### `__str__()`

Retorna a representação em string da exceção.

Returns:
    str: mensagem da exceção

**Parâmetros:**

- `self` (Any)

**Retorna:** str

## Classe: `UpdateError`

Exception raised when trying to update the user itself.

**Herda de:** `Exception`

### Métodos

#### `__init__()`

Initialize the exception.

**Parâmetros:**

- `self` (Any)
- `exc` (Exception | None)
- `message` (str | None)

#### `__str__()`

Retorna a representação em string da exceção.

Returns:
    str: mensagem da exceção

**Parâmetros:**

- `self` (Any)

**Retorna:** str

## Classe: `InsertError`

Exception raised when trying to insert the user itself.

**Herda de:** `Exception`

### Métodos

#### `__init__()`

Initialize the exception.

**Parâmetros:**

- `self` (Any)
- `exc` (Exception | None)
- `message` (str | None)

#### `__str__()`

Retorna a representação em string da exceção.

Returns:
    str: mensagem da exceção

**Parâmetros:**

- `self` (Any)

**Retorna:** str

