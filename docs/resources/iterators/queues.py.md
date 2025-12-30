# resources/iterators/queues.py

## Propósito

Implemente iteradores para filas do tipo Queue.

Este módulo fornece o iterador QueueIterator para acesso
sequencial aos elementos de uma fila, tratando exceções
de fila vazia ou encerrada.

## Dependências Principais

- `queue`
- `typing`

## Classe: `QueueIterator`

Implemente iterador para filas do tipo Queue.

Permite acesso sequencial aos elementos da fila,
tratando exceções de fila vazia ou encerrada.

### Métodos

#### `__init__()`

Inicialize o iterador com a fila fornecida.

Args:
    queue (Queue): Fila a ser iterada.

**Parâmetros:**

- `self` (Any)
- `queue` (Queue)

#### `__iter__()`

Retorne o próprio iterador.

Returns:
    Self: O próprio iterador.

**Parâmetros:**

- `self` (Any)

**Retorna:** Self

#### `__next__()`

Retorne o próximo elemento da fila ou None se vazia.

Returns:
    T: Próximo elemento da fila ou None se vazia.

Raises:
    StopIteration: Se a fila estiver encerrada.

**Parâmetros:**

- `self` (Any)

**Retorna:** T

