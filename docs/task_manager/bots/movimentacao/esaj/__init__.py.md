# task_manager/bots/movimentacao/esaj/__init__.py

## Propósito

Implemente a raspagem de movimentações do ESAJ.

Este pacote contém classes e funções para coletar e filtrar
movimentações processuais do sistema ESAJ.

## Dependências Principais

- `__future__`
- `backend.common.raises`
- `backend.controllers.esaj`
- `backend.resources.elements`
- `contextlib`
- `re`
- `selenium.common.exceptions`
- `selenium.webdriver.common.by`
- `selenium.webdriver.support`
- `typing`

## Constantes

- `SUCESSO`
- `SIZE_ITEMSMOVE`

## Classe: `Movimentacao`

Raspagem de movimentações esaj.

**Herda de:** `ESajBot`

### Métodos

#### `execution()`

Executa a raspagem das movimentações do processo no ESAJ.

**Parâmetros:**

- `self` (Any)

#### `queue()`

Execute a fila de raspagem das movimentações do ESAJ.

Raises:
    ExecutionError: Caso ocorra erro na execução da fila.

**Parâmetros:**

- `self` (Any)

#### `setup_config()`

Configure e filtre as movimentações conforme os parâmetros.

Raises:
    ExecutionError: Caso nenhuma movimentação seja encontrada.

**Parâmetros:**

- `self` (Any)

#### `filter_moves()`

Filtre movimentações conforme critérios definidos.

Args:
    move (WebElement): Elemento da movimentação.

Returns:
    bool: True se atender aos critérios, False caso contrário.

**Parâmetros:**

- `self` (Any)
- `move` (WebElement)

**Retorna:** bool

#### `data_check()`

Verifique se a data da movimentação está no intervalo definido.

Args:
    data_mov (str): Data da movimentação a ser verificada.

Returns:
    bool: True se a data estiver no intervalo, False caso contrário.

**Parâmetros:**

- `self` (Any)
- `data_mov` (str)

**Retorna:** bool

#### `text_check()`

Verifique se o texto da movimentação contém a palavra-chave.

Args:
    text_mov (str): Texto da movimentação.
    keyword (str): Palavra-chave para busca.

Returns:
    bool: True se o texto corresponder, False caso contrário.

**Parâmetros:**

- `self` (Any)
- `text_mov` (str)
- `keyword` (str)

**Retorna:** bool

#### `check_intimado()`

Verifique se o texto menciona o intimado especificado.

Args:
    text_mov (str): Texto da movimentação.

Returns:
    bool: True se o intimado for mencionado, False caso contrário.

**Parâmetros:**

- `self` (Any)
- `text_mov` (str)

**Retorna:** bool

#### `scrap_moves()`

Filtre e processe movimentações conforme a palavra-chave.

Args:
    keyword (str): Palavra-chave para filtrar movimentações.

**Parâmetros:**

- `self` (Any)
- `keyword` (str)

#### `_log_scrap_moves_header()`

Gera e exibe o cabeçalho de log para a busca de movimentações.

Args:
    keyword (str): Palavra-chave utilizada na busca.

**Parâmetros:**

- `self` (Any)
- `keyword` (str)

#### `_check_others()`

Realiza verificações adicionais para a movimentação.

Args:
    text_mov (str): Texto da movimentação.

Returns:
    tuple: Flags e informações auxiliares para processamento.

**Parâmetros:**

- `self` (Any)
- `text_mov` (str)

**Retorna:** tuple[bool, bool, str, bool, bool]

#### `process_single_move()`

Processa uma única movimentação filtrada.

Args:
    move: Elemento de movimentação.
    keyword (str): Palavra-chave utilizada na busca.

**Parâmetros:**

- `self` (Any)
- `move` (WebElement)
- `keyword` (str)

#### `set_page_size()`

Set the page size for movement scraping.

**Parâmetros:**

- `self` (Any)

#### `set_tablemoves()`

Set the table moves element.

**Parâmetros:**

- `self` (Any)

#### `get_moves()`

Retrieve movement information.

Extracts and appends movement details from the page elements.

# Inline: Scroll to element, reveal table, then iterate through rows.

**Parâmetros:**

- `self` (Any)

