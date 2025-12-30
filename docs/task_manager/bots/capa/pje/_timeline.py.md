# task_manager/bots/capa/pje/_timeline.py

## Propósito

Módulo do sistema CrawJUD.

## Dependências Principais

- `__future__`
- `backend.controllers`
- `backend.task_manager.bots.capa.pje._dicionarios`
- `collections`
- `contextlib`
- `datetime`
- `httpx`
- `typing`
- `zoneinfo`

## Constantes

- `TZ_SAO_PAULO`

## Classe: `LinkPJe`

**Herda de:** `UserString`

### Métodos

#### `__init__()`

**Parâmetros:**

- `self` (Any)
- `regiao` (str)
- `id_proc` (str)
- `query` (dict)
- `endpoint` (str)

#### `__repr__()`

**Parâmetros:**

- `self` (Any)

**Retorna:** ReprLinkTimeline

## Classe: `NomeDocumentoPJe`

**Herda de:** `UserString`

### Métodos

#### `__init__()`

**Parâmetros:**

- `self` (Any)
- `tl` (TimeLinePJe)
- `documento` (DocumentoPJe)

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
- `bot` (PJeBot)
- `documento` (DocumentoPJe)
- `grau` (str)

**Retorna:** bytes

