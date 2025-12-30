# task_manager/tasks/database.py

## Propósito

Gerencie tarefas relacionadas ao banco de dados e execuções de bots.

Este módulo define tarefas para iniciar e finalizar execuções de bots,
utilizando integração com Celery e SQLAlchemy.

## Dependências Principais

- `__future__`
- `backend.extensions`
- `backend.models`
- `backend.task_manager.decorators`
- `backend.task_manager.tasks.base`
- `datetime`
- `flask`
- `flask_sqlalchemy`
- `typing`
- `zoneinfo`

## Constantes

- `TIMEZONE`

## Classe: `DatabaseTasks`

Gerencie tarefas relacionadas ao banco de dados.

Esta classe executa operações de controle de execuções de bots.

**Herda de:** `BotTasks`

### Métodos

#### `informacao_database()`

Gerencie início ou fim de execução de bot no banco.

Args:
    app (Flask): Instância da aplicação Flask.
    bot_id (int): ID do bot a ser executado.
    user_id (int): ID do usuário responsável.
    pid (str): Identificador do processo.
    operacao (Literal["start", "stop"]): Operação desejada.

Returns:
    str: Mensagem de sucesso da operação.

**Parâmetros:**

- `cls` (Any)
- `app` (Flask)
- `bot_id` (int)
- `user_id` (int)
- `pid` (str)
- `operacao` (Literal['start', 'stop'])

**Retorna:** Literal['Operação de banco de dados concluída com sucesso!']

