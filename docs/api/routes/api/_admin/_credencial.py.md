# api/routes/api/_admin/_credencial.py

## Propósito

Módulo do sistema CrawJUD.

## Dependências Principais

- `__future__`
- `backend.models`
- `backend.types_app`
- `contextlib`
- `flask_jwt_extended`
- `flask_keepass`
- `pathlib`
- `pykeepass.group`
- `typing`
- `uuid`

## Classe: `CredencialBotDict`

**Herda de:** `TypedDict`

### Atributos

- `nome_credencial` (str)
- `sistema` (Sistemas)
- `login_metodo` (LoginMetodoSimplificado)
- `login` (str | None)
- `password` (str | None)
- `certificado` (FileStorage | None)
- `cpf_cnpj_certificado` (str | None)
- `senha_certificado` (str | None)
- `otp` (str | None)
- `requer_duplo_fator` (bool)

## Classe: `CredencialBot`

### Atributos

- `nome_credencial` (str)
- `sistema` (Sistemas)
- `login_metodo` (LoginMetodoSimplificado)
- `login` (str | None)
- `password` (str | None)
- `certificado` (FileStorage | None)
- `cpf_cnpj_certificado` (str | None)
- `senha_certificado` (str | None)
- `otp` (str | None)
- `requer_duplo_fator` (bool)
- `db` (SQLAlchemy)

### Métodos

#### `__init__()`

**Parâmetros:**

- `self` (Any)
- `app` (Flask)

#### `cadastro()`

**Parâmetros:**

- `self` (Any)

#### `deletar_credencial()`

**Parâmetros:**

- `cls` (Any)

