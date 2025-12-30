# controllers/esaj.py

## Propósito

Módulo para a classe de controle dos robôs ESaj.

## Dependências Principais

- `backend.controllers.head`
- `backend.resources.elements`
- `contextlib`
- `pathlib`
- `selenium.common.exceptions`
- `selenium.webdriver.common.by`
- `selenium.webdriver.support`
- `selenium.webdriver.support.ui`
- `string`
- `time`

## Classe: `ESajBot`

Classe de controle para robôs do ESaj.

**Herda de:** `CrawJUD`

### Métodos

#### `auth()`

Realize a autenticação do usuário no sistema ESaj.

Returns:
    bool: Indica se a autenticação foi bem-sucedida.

**Parâmetros:**

- `self` (Any)

**Retorna:** bool

