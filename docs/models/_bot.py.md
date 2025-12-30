# models/_bot.py

## Propósito

Modulo de controle da model bots.

## Dependências Principais

- `__future__`
- `backend.extensions`
- `backend.models._users`
- `datetime`
- `sqlalchemy`
- `sqlalchemy.orm`
- `typing`

## Classe: `Bots`

**Herda de:** `db.Model`

### Atributos

- `__table_args__` (ClassVar[_TableArgs])
- `Id` (int)
- `display_name` (str)
- `sistema` (str)
- `categoria` (str)
- `configuracao_form` (str)
- `descricao` (str)
- `license_id` (int)
- `license_` (Mapped[LicenseUser])
- `execucoes` (Mapped[list[ExecucoesBot]])

## Classe: `ExecucoesBot`

Model de execuções dos bots.

**Herda de:** `db.Model`

### Atributos

- `__table_args__` (ClassVar[_TableArgs])
- `Id` (int)
- `pid` (str)
- `status` (str)
- `data_inicio` (datetime)
- `data_fim` (datetime)
- `user_id` (int)
- `usuario` (Mapped[User])
- `bot_id` (int)
- `bot` (Mapped[Bots])

## Classe: `CredenciaisRobo`

Credenciais Bots Model.

**Herda de:** `db.Model`

### Atributos

- `__table_args__` (ClassVar[_TableArgs])
- `Id` (int)
- `nome_credencial` (str)
- `sistema` (str)
- `login_metodo` (str)
- `rastreio` (str)
- `license_id` (int)
- `license_` (Mapped[LicenseUser])

