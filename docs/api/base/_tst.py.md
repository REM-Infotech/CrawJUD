# api/base/_tst.py

## Propósito

Módulo do sistema CrawJUD.

## Dependências Principais

- `__future__`
- `backend.types_app`
- `re`
- `typing`

## Classe: `CustomPattern`

### Métodos

#### `__init__()`

**Parâmetros:**

- `self` (Any)
- `pattern` (str)
- `flags` (int)

#### `match()`

**Parâmetros:**

- `self` (Any)
- `text` (str)

**Retorna:** re.Match[str] | None

#### `search()`

**Parâmetros:**

- `self` (Any)
- `text` (str)

**Retorna:** re.Match[str] | None

#### `fullmatch()`

**Parâmetros:**

- `self` (Any)
- `text` (str)

**Retorna:** re.Match[str] | None

#### `findall()`

**Parâmetros:**

- `self` (Any)
- `text` (str)

**Retorna:** list[AnyType]

#### `sub()`

**Parâmetros:**

- `self` (Any)
- `repl` (str)
- `text` (str)

**Retorna:** str

#### `__repr__()`

**Parâmetros:**

- `self` (Any)

**Retorna:** str

