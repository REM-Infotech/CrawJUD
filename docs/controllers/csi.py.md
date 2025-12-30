# controllers/csi.py

## Propósito

Módulo para a classe de controle dos robôs PROJUDI.

## Dependências Principais

- `backend.controllers.head`
- `backend.resources.elements`
- `contextlib`
- `selenium.webdriver.common.by`
- `selenium.webdriver.support`

## Classe: `CsiBot`

Classe de controle para robôs do CSI.

**Herda de:** `CrawJUD`

### Métodos

#### `search()`

Realiza uma busca no sistema CSI.

**Retorna:** bool

#### `auth()`

Realiza autenticação no sistema CSI.

Returns:
    bool: Indica se a autenticação foi bem-sucedida.

**Parâmetros:**

- `self` (Any)

**Retorna:** bool

