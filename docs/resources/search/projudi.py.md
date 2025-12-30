# resources/search/projudi.py

## Propósito

Implemente buscas de processos no sistema PROJUDI.

Este módulo contém a classe ProjudiSearch e funções auxiliares
para pesquisar, acessar e manipular processos judiciais no PROJUDI.

## Dependências Principais

- `__future__`
- `backend.controllers.projudi`
- `backend.interfaces`
- `backend.resources.elements`
- `backend.resources.search.main`
- `contextlib`
- `selenium.common.exceptions`
- `selenium.webdriver.support`
- `selenium.webdriver.support.ui`
- `typing`

## Constantes

- `GRAU_PRIMEIRA_INSTANCIA`
- `GRAU_SEGUNDA_INSTANCIA`

## Classe: `ProjudiSearch`

Implemente buscas de processos no sistema PROJUDI.

Atributos:
    bot (ProjudiBot): Bot controlador do PROJUDI.
    bot_data (BotData): Dados do processo a ser buscado.
    url_segunda_instancia (str): URL para busca em 2ª instância.

Métodos:
    __call__(): Executa a busca do processo.
    search_proc(): Pesquisa processo no PROJUDI.
    detect_intimacao(): Verifica intimação pendente.
    allow_access(): Permite acesso ao processo.
    get_link_grau2(): Obtém link de recursos do grau 2.

**Herda de:** `SearchBot`

### Atributos

- `bot` (ProjudiBot)
- `bot_data` (BotData)
- `url_segunda_instancia` (str)

### Métodos

#### `__call__()`

Procura processos no PROJUDI.

Returns:
    bool: True se encontrado; ou False
redireciona pra cada rota apropriada

**Parâmetros:**

- `self` (Any)

**Retorna:** bool

#### `search_proc()`

Pesquisa processo no PROJUDI.

Returns:
    bool: True se encontrado; ou False
manipula entradas, clique e tentativa condicional

**Parâmetros:**

- `self` (Any)

**Retorna:** bool

#### `__consultar_processo()`

**Parâmetros:**

- `self` (Any)
- `numero_processo` (str)
- `grau` (int)

#### `_verifica_processo_encontrado()`

**Parâmetros:**

- `self` (Any)

**Retorna:** WebElement | None

#### `__acessar_processo()`

**Parâmetros:**

- `self` (Any)

#### `detect_intimacao()`

**Parâmetros:**

- `self` (Any)

#### `allow_access()`

Permite acesso provisório ao processo no sistema PROJUDI.

Args:
    driver (WebDriver): Instância do navegador Selenium WebDriver.

Executa cliques para habilitar acesso provisório e aceitar termos.

**Parâmetros:**

- `self` (Any)

#### `get_link_grau2()`

Retorne link de recursos do grau 2 do processo.

Args:
    wait (WebDriverWait): Espera explícita do Selenium.

Returns:
    str | None: Link encontrado ou None.

**Parâmetros:**

- `self` (Any)

**Retorna:** str | None

