# task_manager/tasks/base.py

## Propósito

Gerencie tarefas e utilitários para bots e execuções.

Este módulo fornece classes e funções para manipular bots,
usuários, execuções e templates de e-mail.

## Dependências Principais

- `__future__`
- `backend.models`
- `flask`
- `flask_sqlalchemy`
- `jinja2`
- `jinja2.environment`
- `pathlib`
- `typing`
- `zoneinfo`

## Constantes

- `PARENT_PATH`
- `TEMPLATES_PATH`
- `TIMEZONE`

## Classe: `BotTasks`

Gerencie tarefas relacionadas a bots e consultas ao banco.

Esta classe fornece métodos utilitários para manipular bots,
usuários e execuções, além de gerenciar templates de e-mail.

### Atributos

- `notificacoes` (ClassVar[dict[str, JinjaTemplate]])

### Métodos

#### `sqlalchemy_instance()`

Retorne a instância do SQLAlchemy do app Flask fornecido.

Args:
    app (Flask): Instância da aplicação Flask.

Returns:
    SQLAlchemy: Instância do SQLAlchemy associada ao app.

**Parâmetros:**

- `cls` (Any)
- `app` (Flask)

**Retorna:** SQLAlchemy

#### `query_bot()`

Consulte e retorne um bot pelo ID informado.

Args:
    db (SQLAlchemy): Instância do banco de dados SQLAlchemy.
    bot_id (int): Identificador do bot.

Returns:
    Bots | None: Bot encontrado ou None se não existir.

**Parâmetros:**

- `cls` (Any)
- `db` (SQLAlchemy)
- `bot_id` (int)

**Retorna:** Bots | None

#### `query_user()`

Consulte e retorne um usuário pelo ID informado.

Args:
    db (SQLAlchemy): Instância do banco de dados SQLAlchemy.
    user_id (int): Identificador do usuário.

Returns:
    User | None: Usuário encontrado ou None se não existir.

**Parâmetros:**

- `cls` (Any)
- `db` (SQLAlchemy)
- `user_id` (int)

**Retorna:** User | None

#### `query_execucao()`

Consulte e retorne uma execução pelo PID informado.

Args:
    db (SQLAlchemy): Instância do banco de dados SQLAlchemy.
    pid (str): Identificador do processo.

Returns:
    ExecucoesBot | None: Execução encontrada ou None se não existir.

**Parâmetros:**

- `cls` (Any)
- `db` (SQLAlchemy)
- `pid` (str)

**Retorna:** ExecucoesBot | None

