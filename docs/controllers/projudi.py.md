# controllers/projudi.py

## Propósito

Módulo para a classe de controle dos robôs PROJUDI.

## Dependências Principais

- `__future__`
- `backend.controllers.head`
- `backend.resources`
- `backend.resources.auth.projudi`
- `backend.resources.formatadores`
- `backend.resources.search.projudi`
- `bs4`
- `bs4._typing`
- `typing`

## Classe: `ProjudiBot`

Classe de controle para robôs do PROJUDI.

**Herda de:** `CrawJUD`

### Atributos

- `url_segunda_instancia` (str)
- `rows_data` (_SomeTags)

### Métodos

#### `__init__()`

Inicialize o robô PROJUDI e seus componentes.

**Parâmetros:**

- `self` (Any)

#### `parse_data()`

Extrai dados do HTML do processo.

Args:
    inner_html (str): HTML da página do processo.

Returns:
    dict[str, str]: Dados extraídos do processo.

**Parâmetros:**

- `self` (Any)
- `inner_html` (str)

**Retorna:** dict[str, str]

#### `get_text()`

Retorne o texto normalizado da próxima célula.

Args:
    pos (int): Posição do elemento na lista de linhas.

Returns:
    str | None: Texto encontrado ou None se não houver.

**Parâmetros:**

- `self` (Any)
- `pos` (int)

**Retorna:** str | None

