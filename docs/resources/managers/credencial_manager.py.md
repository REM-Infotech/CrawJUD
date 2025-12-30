# resources/managers/credencial_manager.py

## Propósito

Gerenciador de credenciais CrawJUD.

## Dependências Principais

- `__future__`
- `backend.controllers.head`
- `base64`
- `pathlib`
- `typing`

## Classe: `CredencialManager`

Gerenciador de credenciais CrawJUD.

### Atributos

- `_username` (str)
- `_password` (str)
- `_certificado` (Path)
- `_kdbx` (Path)

### Métodos

#### `__init__()`

Instancia da gestão de credenciais.

**Parâmetros:**

- `self` (Any)
- `bot` (CrawJUD)

#### `load_credenciais()`

Carregue credenciais do dicionário de configuração.

Args:
    config (dict): Dicionário com usuário e senha.

**Parâmetros:**

- `self` (Any)
- `config` (dict[str, str])

#### `username()`

Retorne o nome de usuário carregado.

**Parâmetros:**

- `self` (Any)

**Retorna:** str

#### `password()`

Retorne a senha carregada.

**Parâmetros:**

- `self` (Any)

**Retorna:** str

#### `certificado()`

**Parâmetros:**

- `self` (Any)

**Retorna:** Path

#### `otp()`

**Parâmetros:**

- `self` (Any)

**Retorna:** str

