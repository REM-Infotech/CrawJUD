# resources/iterators/pje.py

## Propósito

Módulo de agrupamento de Iterators para o CrawJUD.

## Dependências Principais

- `__future__`
- `backend.common.exceptions.validacao`
- `backend.controllers.pje`
- `backend.interfaces`
- `backend.types_app.bot`
- `typing`

## Classe: `DictSeparaRegiao`

Define o dicionário que separa regiões e posições de processos.

Args:
    regioes (dict[str, list[BotData]]): Dicionário de regiões e bots.
    position_process (dict[str, int]): Posição dos processos por região.

**Herda de:** `TypedDict`

### Atributos

- `regioes` (dict[str, list[BotData]])
- `position_process` (dict[ProcessoCNJ, int])

## Classe: `RegioesIterator`

Retorne regiões e dados associados iterando sobre processos separados.

Args:
    bot (PJeBot): Instância do bot para acessar métodos e dados.

Returns:
    RegioesIterator: Iterador sobre tuplas (região, dados da região).

Raises:
    StopIteration: Quando todas as regiões forem iteradas.

### Métodos

#### `__init__()`

Inicialize o iterador de regiões.

Args:
    bot (PJeBot): Instância do bot para acessar métodos e dados.

**Parâmetros:**

- `self` (Any)
- `bot` (PJeBot)

#### `__iter__()`

Retorne o próprio iterador para permitir iteração sobre regiões.

Returns:
    RegioesIterator: O próprio iterador de regiões.

**Parâmetros:**

- `self` (Any)

**Retorna:** RegioesIterator[list[T]]

#### `__next__()`

Implementa a iteração retornando próxima região e dados associados.

Returns:
    tuple[str, str]: Tupla contendo a região e os dados da região.

Raises:
    StopIteration: Quando todas as regiões forem iteradas.

**Parâmetros:**

- `self` (Any)

**Retorna:** T

#### `separar_regiao()`

Separa os processos por região a partir do número do processo.

Returns:
    dict[str, list[BotData] | dict[str, int]]: Dicionário com as
    regiões e a posição de cada processo.

**Parâmetros:**

- `self` (Any)

**Retorna:** DictSeparaRegiao

