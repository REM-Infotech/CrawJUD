# task_manager/decorators/__init__.py

## Propósito

Fornece decoradores para tarefas compartilhadas com Celery.

## Dependências Principais

- `__future__`
- `asyncio`
- `backend.config`
- `backend.task_manager.base`
- `backend.task_manager.proto`
- `backend.types_app`
- `celery`
- `collections.abc`
- `importlib`
- `typing`

## Classe: `SharedClassMethodTask`

Defina decorador para criar tarefas Celery de classmethods.

Args:
    name (str): Nome da tarefa.
    bind (bool): Se deve vincular a instância.
    base (object | None): Classe base da tarefa.

### Métodos

#### `__init__()`

Inicialize o decorador com nome, bind e base da tarefa.

Args:
    name (str): Nome da tarefa.
    bind (bool): Se deve vincular a instância.
    base (object | None): Classe base da tarefa.

**Parâmetros:**

- `self` (Any)
- `name` (str)

#### `__call__()`

Decora classmethod como tarefa Celery compartilhada.

Args:
    fn (Callable[P, T]): Classmethod a ser decorado.

Returns:
    CeleryTask[P, T]: Tarefa Celery decorada.

**Parâmetros:**

- `self` (Any)
- `fn` (Callable[P, T])

**Retorna:** CeleryTask[P, T]

#### `_run()`

Executa o classmethod decorado, suportando async.

Args:
    cls: Classe do classmethod.
    *args (AnyType): Argumentos posicionais.
    **kwargs (AnyType): Argumentos nomeados.

Returns:
    T: Resultado do classmethod.

**Parâmetros:**

- `self` (Any)

**Retorna:** T

## Classe: `SharedTask`

Defina decorador para criar tarefas compartilhadas com Celery.

Args:
    name (str): Nome da tarefa.
    bind (bool): Se deve vincular a instância.
    base (object | None): Classe base da tarefa.

### Métodos

#### `__init__()`

Inicialize o decorador com nome, bind e base da tarefa.

Args:
    name (str): Nome da tarefa.
    bind (bool): Se deve vincular a instância.
    base (object | None): Classe base da tarefa.

**Parâmetros:**

- `self` (Any)
- `name` (str)

#### `__call__()`

Decora função como tarefa Celery compartilhada.

Args:
    fn (Callable[P, T]): Função a ser decorada.

Returns:
    CeleryTask[P, T]: Tarefa Celery decorada.

**Parâmetros:**

- `self` (Any)
- `fn` (Callable[P, T])

**Retorna:** CeleryTask[P, T]

#### `_run()`

**Parâmetros:**

- `self` (Any)

**Retorna:** T

## Função: `import_class()`

Importa e retorne uma classe a partir do caminho informado.

Args:
    path (str): Caminho completo da classe.

Returns:
    object: Classe importada dinamicamente.

**Parâmetros:**

- `path` (str)

**Retorna:** object

### Exemplo de Uso

```python
resultado = import_class(path)
```

