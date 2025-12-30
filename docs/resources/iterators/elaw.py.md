# resources/iterators/elaw.py

## Propósito

Implemente iteradores para manipular dados do ElawBot.

Este módulo fornece classes para iterar sobre dados de entrada
da planilha utilizados pelo ElawBot.

## Dependências Principais

- `__future__`
- `backend.controllers.elaw`
- `backend.interfaces`
- `backend.interfaces.elaw.main`
- `typing`

## Classe: `ElawIterator`

Implemente iteração sobre dados do ElawBot.

### Métodos

#### `__init__()`

Inicialize o iterador com a instância do ElawBot.

Args:
    bot (ElawBot): Instância do ElawBot para iteração.

**Parâmetros:**

- `self` (Any)
- `bot` (ElawBot)

#### `__iter__()`

Retorne o próprio iterador.

Returns:
    Self: O próprio objeto iterador.

**Parâmetros:**

- `self` (Any)

**Retorna:** Self

#### `__next__()`

Retorne o próximo item do iterador.

Returns:
    BotData: Próximo item da iteração.

Raises:
    StopIteration: Quando não houver mais itens.

**Parâmetros:**

- `self` (Any)

**Retorna:** BotData

