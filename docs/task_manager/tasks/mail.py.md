# task_manager/tasks/mail.py

## Propósito

Gerencie tarefas de envio de e-mails para notificações.

Este pacote lida com templates e envio de e-mails para eventos de tarefas.

## Dependências Principais

- `__future__`
- `backend.common.exceptions._fatal`
- `backend.models`
- `backend.task_manager.decorators`
- `backend.task_manager.tasks.base`
- `celery`
- `flask`
- `flask_mail`
- `logging`
- `typing`

## Classe: `MailTasks`

Gerencie tarefas relacionadas ao envio de e-mails.

Esta classe lida com notificações por e-mail para eventos de tarefas.

**Herda de:** `BotTasks`

### Métodos

#### `notifica_email()`

Envie notificação de início de tarefa por e-mail.

Args:
    app (Flask): Instância da aplicação Flask.
    pid (str): Identificador do processo.
    bot_id (int): ID do bot.
    user_id (int): ID do usuário.
    xlsx (str | None): Caminho do arquivo XLSX (opcional).
    tipo_notificacao (Literal["start", "stop"]): Tipo de notificação.
    **kwargs: str | Any
Returns:
    str: Mensagem de sucesso do envio do e-mail.

**Parâmetros:**

- `cls` (Any)
- `app` (Flask)
- `pid` (str)
- `bot_id` (int)
- `user_id` (int)
- `tipo_notificacao` (Literal['start', 'stop'])
- `xlsx` (str | None)

**Retorna:** Literal['E-mail enviado com sucesso!']

