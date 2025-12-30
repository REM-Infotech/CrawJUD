# resources/search/elaw.py

## Propósito

Implemente buscas de processos no sistema Elaw usando Selenium.

Este módulo contém a classe ElawSearch para automação de buscas
e abertura de processos judiciais no sistema Elaw.

## Dependências Principais

- `__future__`
- `backend.resources.driver.web_element`
- `backend.resources.elements`
- `backend.resources.search.main`
- `selenium.common.exceptions`
- `selenium.webdriver.common.by`
- `selenium.webdriver.support`
- `selenium.webdriver.support.wait`
- `time`
- `typing`

## Classe: `ElawSearch`

Realize buscas de processos no sistema Elaw.

**Herda de:** `SearchBot`

### Métodos

#### `__call__()`

Realiza a busca de um processo no sistema Elaw.

Returns:
    bool: Indica se o processo foi encontrado.

**Parâmetros:**

- `self` (Any)

**Retorna:** bool

#### `open_proc()`

Abre o processo encontrado na lista de resultados.

Returns:
    bool: Indica se o processo foi aberto com sucesso.

**Parâmetros:**

- `self` (Any)

**Retorna:** bool

