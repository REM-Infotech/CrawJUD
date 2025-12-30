# task_manager/bots/movimentacao/pje/__init__.py

## Propósito

Módulo do sistema CrawJUD.

## Dependências Principais

- `__future__`
- `backend.controllers.pje`
- `backend.interfaces.pje`
- `backend.resources.driver`
- `backend.types_app`
- `contextlib`
- `queue`
- `tqdm`
- `traceback`
- `typing`

## Constantes

- `THREAD_PREFIX`
- `WORKERS_QTD`

## Classe: `Movimentacao`

**Herda de:** `PJeBot`

### Atributos

- `queue_files` (Queue)
- `driver` (Chrome)

### Métodos

#### `execution()`

**Parâmetros:**

- `self` (Any)

#### `queue_regiao()`

Enfileire processos judiciais para processamento.

Args:
    data (list[PJeMovimentacao]): Lista de dados dos processos.

**Parâmetros:**

- `self` (Any)
- `data` (list[PJeMovimentacao])

#### `set_event()`

**Parâmetros:**

- `self` (Any)

#### `queue()`

Enfileire e processe um processo judicial PJE.

Args:
    item (PJeMovimentacao): Dados do processo.
    client (Client): Cliente HTTP autenticado.

**Parâmetros:**

- `self` (Any)
- `item` (PJeMovimentacao)
- `client` (Client)

#### `extrair_processo()`

**Parâmetros:**

- `self` (Any)
- `item` (PJeMovimentacao)
- `row` (int)
- `client` (Client)
- `termos` (list[str])
- `grau` (str)

#### `kw_timeline()`

**Parâmetros:**

- `self` (Any)
- `result` (DictResults)
- `item` (PJeMovimentacao)
- `client` (Client)

**Retorna:** dict

#### `formata_termos()`

**Parâmetros:**

- `self` (Any)
- `termos` (str)

**Retorna:** list[str]

#### `filtrar_arquivos()`

**Parâmetros:**

- `self` (Any)
- `tl` (TimeLinePJe)
- `termos` (list[str])

**Retorna:** list[DocumentoPJe]

#### `salva_erro()`

**Parâmetros:**

- `self` (Any)
- `row` (int)
- `item` (PJeMovimentacao)

#### `capa_processual()`

Gere a capa processual do processo judicial PJE.

Args:
    result (ProcessoJudicialDict): Dados do processo judicial.

Returns:
    CapaPJe: Dados da capa processual gerados.

**Parâmetros:**

- `self` (Any)
- `result` (Dict)

**Retorna:** CapaPJe

