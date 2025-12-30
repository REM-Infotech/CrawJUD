# config/_log/_handlers.py

## Propósito

Módulo do sistema CrawJUD.

## Dependências Principais

- `logging`
- `typing`

## Classe: `RichQueueHandler`

**Herda de:** `Handler`

### Atributos

- `level` (int)
- `markups` (ClassVar[dict[int, str]])

### Métodos

#### `__init__()`

**Parâmetros:**

- `self` (Any)
- `target` (str)
- `level` (int)

#### `emit()`

**Parâmetros:**

- `self` (Any)
- `record` (LogRecord)

