# common/exceptions/_fatal.py

## Propósito

Módulo do sistema CrawJUD.

## Dependências Principais

- `traceback`
- `typing`

## Classe: `FatalError`

Exceção fatal na execução do bot CrawJUD.

**Herda de:** `Exception`

### Atributos

- `message` (ClassVar[str])

### Métodos

#### `__init__()`

Initialize FatalError with the given exception.

Args:
    exc (Exception): The exception that caused the fatal error.
    msg: Message (Optional)
    *args (AnyType): Additional arguments to pass to the base Exception.

**Parâmetros:**

- `self` (Any)
- `exc` (Exception)

#### `_format()`

**Parâmetros:**

- `self` (Any)

#### `__str__()`

Return the string representation of the FatalError.

**Parâmetros:**

- `self` (Any)

**Retorna:** str

#### `__repr__()`

Return the string representation of the FatalError for debugging.

**Parâmetros:**

- `self` (Any)

**Retorna:** str

#### `__reduce__()`

**Parâmetros:**

- `self` (Any)

**Retorna:** tuple[type[Self], tuple[Exception]]

#### `__getstate__()`

**Parâmetros:**

- `self` (Any)

**Retorna:** dict[str, AnyType]

#### `__setstate__()`

**Parâmetros:**

- `self` (Any)
- `state` (dict[str, AnyType])

