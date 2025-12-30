# task_manager/bots/habilitacao/pje/__init__.py

## Propósito

Módulo do sistema CrawJUD.

## Dependências Principais

- `__future__`
- `backend.common`
- `backend.common.exceptions`
- `backend.controllers`
- `backend.controllers.projudi`
- `backend.interfaces`
- `backend.resources`
- `backend.resources.elements`
- `backend.resources.formatadores`
- `typing`

## Classe: `HabilitacaoDict`

**Herda de:** `TypedDict`

### Atributos

- `NUMERO_PROCESSO` (str)
- `PETICAO_PRINCIPAL` (str)
- `ANEXOS` (str)

## Classe: `HabilitacaoPJe`

**Herda de:** `PJeBot`

### Atributos

- `name` (ClassVar[str])

### Métodos

#### `execution()`

**Parâmetros:**

- `self` (Any)

#### `queue_regiao()`

Enfileire processos judiciais para processamento.

Args:
    data (list[BotData]): Lista de dados dos processos.

**Parâmetros:**

- `self` (Any)
- `data` (list[HabilitacaoDict])

