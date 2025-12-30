# task_manager/base/task.py

## Propósito

Fornece integração de tarefas Celery com contexto Flask.

## Dependências Principais

- `__future__`
- `backend.types_app`
- `celery`
- `typing`

## Classe: `FlaskTask`

Integre tarefas Celery ao contexto Flask nesta classe.

**Herda de:** `Task`

### Métodos

#### `__call__()`

Executa a tarefa Celery dentro do contexto Flask.

Args:
    *args (AnyType): Argumentos posicionais da tarefa.
    **kwargs (AnyType): Argumentos nomeados da tarefa.

Returns:
    AnyType: Resultado da execução da tarefa.

**Parâmetros:**

- `self` (Any)

**Retorna:** AnyType

#### `async _run()`

**Parâmetros:**

- `self` (Any)

**Retorna:** AnyType

