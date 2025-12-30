# resources/auth/pje.py

## Propósito

Autenticador PJe.

## Dependências Principais

- `backend.common`
- `backend.controllers.pje`
- `backend.resources.auth.main`
- `backend.resources.formatadores`
- `backend.resources.keystore`
- `contextlib`
- `pyotp`
- `selenium.common`
- `selenium.webdriver.common.by`
- `uuid`

## Classe: `AutenticadorPJe`

Implemente autenticação no PJe usando certificado digital.

Atributos:
    _chain (list[Certificate]): Cadeia de certificados.
    bot (PJeBot): Instância do bot PJe.

**Herda de:** `AutenticadorBot`

### Atributos

- `_chain` (list[Certificate])
- `bot` (PJeBot)

### Métodos

#### `regiao()`

Retorne a região do bot PJe.

**Parâmetros:**

- `self` (Any)

**Retorna:** str

#### `__init__()`

Inicialize o autenticador PJe com certificado e chave.

Args:
    bot (PJeBot): Instância do bot PJe.

**Parâmetros:**

- `self` (Any)
- `bot` (PJeBot)

#### `__call__()`

Realize o login no PJe e retorne True se for bem-sucedido.

Returns:
    bool: Indica se o login foi realizado com sucesso.

**Parâmetros:**

- `self` (Any)

**Retorna:** bool

#### `_login_certificado()`

**Parâmetros:**

- `self` (Any)

#### `_desafio_duplo_fator()`

**Parâmetros:**

- `self` (Any)

#### `_confirmar_login()`

**Parâmetros:**

- `self` (Any)

**Retorna:** bool

#### `get_cookies()`

Retorne os headers e cookies atuais do navegador.

**Parâmetros:**

- `self` (Any)

**Retorna:** dict[str, str]

#### `_cookie_to_dict()`

**Parâmetros:**

- `self` (Any)

**Retorna:** dict[str, str]

#### `_get_otp_uri()`

**Parâmetros:**

- `self` (Any)

**Retorna:** str

