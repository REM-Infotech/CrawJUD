# task_manager/bots/movimentacao/pje/_timeline.py

## Propósito

Módulo do sistema CrawJUD.

## Dependências Principais

- `__future__`
- `_dicionarios`
- `_strings`
- `backend.controllers`
- `contextlib`
- `httpx`
- `typing`

## Constantes

- `BUFFER_1MB`
- `CHUNK_8MB`

## Classe: `TimeLinePJe`

### Atributos

- `documentos` (list[DocumentoPJe])

### Métodos

#### `__init__()`

**Parâmetros:**

- `self` (Any)
- `id_processo` (str)
- `regiao` (str)
- `processo` (str)
- `cliente` (Client)
- `bot` (PJeBot)

#### `load()`

**Parâmetros:**

- `cls` (Any)
- `bot` (PJeBot)
- `cliente` (Client)
- `id_processo` (int | str)
- `regiao` (str)
- `processo` (str)

**Retorna:** Self

#### `baixar_documento()`

**Parâmetros:**

- `self` (Any)
- `documento` (DocumentoPJe)
- `grau` (str)
- `row` (int)

