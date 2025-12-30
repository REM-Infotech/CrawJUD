# controllers/elaw.py

## Propósito

Módulo para a classe de controle dos robôs Elaw.

## Dependências Principais

- `__future__`
- `backend.common.raises`
- `backend.controllers.head`
- `backend.task_manager.constants.data._bots.cidades`
- `contextlib`
- `pathlib`
- `selenium.common.exceptions`
- `selenium.webdriver.support`
- `selenium.webdriver.support.wait`
- `typing`

## Classe: `ElawBot`

Classe de controle para robôs do Elaw.

**Herda de:** `CrawJUD`

### Métodos

#### `__init__()`

Inicialize o robô Elaw.

**Parâmetros:**

- `self` (Any)

#### `elaw_formats()`

Formata e ajuste os dados para uso no Elaw.

Args:
    data (dict[str, str]): Dados a serem formatados.

Returns:
    dict[str, str]: Dados formatados para o Elaw.

**Parâmetros:**

- `self` (Any)
- `data` (dict[str, str])

**Retorna:** dict[str, str]

#### `sleep_load()`

Aguarde até que o elemento de carregamento desapareça.

**Parâmetros:**

- `self` (Any)
- `element` (str)

#### `wait_fileupload()`

Aguarde até que o upload do arquivo seja concluído.

**Parâmetros:**

- `self` (Any)

#### `screenshot_iframe()`

Capture e salve um print da página em um novo iframe.

Args:
    url_page (str): URL da página a ser capturada.
    path_comprovante (Path): Caminho para salvar o print.

**Parâmetros:**

- `self` (Any)
- `url_page` (str)
- `path_comprovante` (Path)

#### `select2()`

Selecione uma opção em campo select2 pelo texto informado.

Args:
    element (WebElement): Elemento select2 alvo.
    to_search (str): Texto da opção a ser selecionada.

**Parâmetros:**

- `self` (Any)
- `element` (WebElement)
- `to_search` (str)

