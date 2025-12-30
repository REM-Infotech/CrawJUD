# resources/iterators/__init__.py

## Propósito

Iterator para os dados inputados na planilha.

## Dependências Principais

- `__future__`
- `backend.controllers.head`
- `backend.interfaces`
- `backend.resources.formatadores`
- `pandas`
- `typing`

## Classe: `BotIterator`

Iterator para os dados inputados na planilha.

### Métodos

#### `__init__()`

Instancia o iterator para os dados inputados na planilha.

**Parâmetros:**

- `self` (Any)
- `bot` (CrawJUD)

#### `__iter__()`

Retorne o próprio iterador para permitir iteração sobre regiões.

Returns:
    RegioesIterator: O próprio iterador de regiões.

**Parâmetros:**

- `self` (Any)

**Retorna:** Self[T]

#### `__next__()`

Implementa a iteração retornando próxima região e dados associados.

Returns:
    tuple[str, str]: Tupla contendo a região e os dados da região.

Raises:
    StopIteration: Quando todas as regiões forem iteradas.

**Parâmetros:**

- `self` (Any)

**Retorna:** T

