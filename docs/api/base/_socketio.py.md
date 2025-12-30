# api/base/_socketio.py

## Propósito

Módulo do sistema CrawJUD.

## Dependências Principais

- `__future__`
- `collections.abc`
- `flask_socketio`
- `functools`
- `typing`

## Constantes

- `P`

## Classe: `BlueprintNamespace`

**Herda de:** `Namespace`

### Métodos

#### `__init__()`

**Parâmetros:**

- `self` (Any)
- `namespace` (str)

#### `on()`

**Parâmetros:**

- `self` (Any)
- `event` (str)

**Retorna:** Callable[[Callable[P, T]], Callable[P, T]]

#### `on()`

**Parâmetros:**

- `self` (Any)
- `event` (str)
- `handler` (Callable[P, T])

**Retorna:** Callable[P, T]

#### `on()`

**Parâmetros:**

- `self` (Any)
- `event` (str)
- `handler` (Callable[P, T] | None)

**Retorna:** Callable[P, T] | Callable[[Callable[P, T]], Callable[P, T]]

#### `event()`

**Parâmetros:**

- `self` (Any)
- `fn` (Callable[P, T])

**Retorna:** Callable[P, T]

#### `_event_register()`

**Parâmetros:**

- `self` (Any)
- `event_name` (str)
- `fn` (Callable[P, T])

**Retorna:** Callable[P, T]

#### `_formata_nome_evento()`

**Parâmetros:**

- `cls` (Any)
- `nome` (str)

**Retorna:** str

