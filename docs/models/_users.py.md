# models/_users.py

## Propósito

Módulo do sistema CrawJUD.

## Dependências Principais

- `__future__`
- `backend.api`
- `backend.models._bot`
- `bcrypt`
- `contextlib`
- `re`
- `sqlalchemy`
- `sqlalchemy.orm`
- `typing`
- `uuid`

## Classe: `LicenseUser`

**Herda de:** `db.Model`

### Atributos

- `__table_args__` (ClassVar[_TableArgs])
- `Id` (int)
- `ProductKey` (str)
- `descricao` (int)
- `Nome` (str)
- `CPF` (str)
- `CNPJ` (str)
- `bots` (Mapped[list[Bots]])
- `usuarios` (Mapped[list[User]])
- `credenciais` (Mapped[list[CredenciaisRobo]])

## Classe: `User`

**Herda de:** `db.Model`

### Atributos

- `__table_args__` (ClassVar[_TableArgs])
- `Id` (int)
- `login` (str)
- `nome_usuario` (str)
- `email` (str)
- `password` (str)
- `admin` (bool)
- `execucoes` (Mapped[list[ExecucoesBot]])
- `license_id` (int)
- `license_` (Mapped[LicenseUser])

### Métodos

#### `authenticate()`

**Parâmetros:**

- `cls` (Any)
- `username` (str)
- `password` (str)

**Retorna:** bool

#### `senhacrip()`

**Parâmetros:**

- `self` (Any)

**Retorna:** str

#### `senhacrip()`

**Parâmetros:**

- `self` (Any)
- `senha_texto` (str)

#### `check_password()`

**Parâmetros:**

- `self` (Any)
- `senha_texto_claro` (str)

**Retorna:** bool

## Função: `_generate_key()`

**Retorna:** str

### Exemplo de Uso

```python
resultado = _generate_key()
```

