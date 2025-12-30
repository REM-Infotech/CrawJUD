# resources/auth/projudi.py

## Propósito

Autenticador PROJUDI.

## Dependências Principais

- `__future__`
- `backend.resources.auth.pje`
- `backend.resources.elements`
- `contextlib`
- `selenium.common.exceptions`
- `selenium.webdriver.common.alert`
- `selenium.webdriver.support`
- `selenium.webdriver.support.ui`
- `time`
- `typing`

## Classe: `AutenticadorProjudi`

Implemente autenticação no sistema PROJUDI.

**Herda de:** `AutenticadorBot`

### Métodos

#### `__call__()`

Autentique usuário no sistema PROJUDI.

Returns:
    bool: True se login bem-sucedido, False caso contrário.

Raises:
    LoginSystemError: Se ocorrer erro na autenticação.

**Parâmetros:**

- `self` (Any)

**Retorna:** bool

