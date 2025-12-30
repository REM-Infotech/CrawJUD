# task_manager/bots/movimentacao/projudi/__init__.py

## Propósito

Module: movimentacao.

Handle movement-related operations in the Projudi system with data scraping and reporting.

## Dependências Principais

- `__future__`
- `backend.controllers.projudi`
- `backend.resources.elements`
- `contextlib`
- `httpx`
- `pathlib`
- `pypdf`
- `selenium.webdriver.support`
- `selenium.webdriver.support.ui`
- `typing`

## Classe: `Movimentacao`

Raspagem de movimentações projudi.

**Herda de:** `ProjudiBot`

### Atributos

- `movimentacao_encontrada` (ClassVar[bool])
- `list_movimentacoes_extraidas` (ClassVar[list[dict[str, str]]])

### Métodos

#### `execution()`

Execute o processamento das linhas de dados e trate erros de movimentação.

Percorra as entradas do frame de dados, processando cada movimentação e
gerenciando possíveis exceções durante a execução.

**Parâmetros:**

- `self` (Any)

#### `queue()`

Gerencie a fila de operações de movimentação e realize a raspagem de dados.

Raises:
    ExecutionError: Caso ocorra falha durante o processamento da fila.

**Parâmetros:**

- `self` (Any)

#### `set_page_size()`

Defina o tamanho da página da tabela de movimentações para 1000 registros.

**Parâmetros:**

- `self` (Any)

#### `extrair_movimentacoes()`

Extraia e processe as movimentações do processo no sistema Projudi.

Realize a raspagem das movimentações do processo atualmente selecionado,
processando e armazenando os dados relevantes para análise posterior.

**Parâmetros:**

- `self` (Any)

#### `__iter_movimentacoes()`

Itera sobre as movimentações filtradas e processe cada uma conforme regras.

Args:
    table_movimentacoes (WebElement): Elemento da tabela de movimentações.
    filtered_moves (list[WebElement]): Lista de linhas filtradas.
    com_documento (bool, opcional): Indica se deve extrair arquivos. Padrão: False.

**Parâmetros:**

- `self` (Any)
- `table_movimentacoes` (WebElement)
- `filtered_moves` (list[WebElement])

#### `_extrair_arquivos_movimentacao()`

Extraia arquivos vinculados à movimentação do processo no Projudi.

Args:
    table_movimentacoes (WebElement): Elemento da tabela de movimentações.
    tds (list[WebElement]): Lista de elementos <td> da movimentação.

**Parâmetros:**

- `self` (Any)
- `table_movimentacoes` (WebElement)
- `tds` (list[WebElement])

#### `_formatar_dados()`

Formata e armazene os dados da movimentação extraída do Projudi.

Args:
    tds (list[WebElement]): Lista de elementos `<td>` da movimentação.

**Parâmetros:**

- `self` (Any)
- `tds` (list[WebElement])

