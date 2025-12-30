# task_manager/bots/movimentacao/pje/_strings.py

## Propósito

Módulo do sistema CrawJUD.

## Dependências Principais

- `__future__`
- `_dicionarios`
- `_timeline`
- `_typing`
- `collections`
- `datetime`
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

