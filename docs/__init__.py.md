# __init__.py

## Propósito

Inicie a aplicação Flask e o servidor SocketIO.

Este script é o ponto de entrada principal para a API. Ele cria a aplicação,
carrega as rotas e executa o servidor SocketIO na porta definida.

## Dependências Principais

- `__future__`
- `backend.api`
- `backend.task_manager`
- `celery`
- `celery.apps.worker`
- `clear`
- `dotenv`
- `flask_socketio`
- `typer`
- `typing`

## Função: `_api()`

### Exemplo de Uso

```python
_api()
```

## Função: `_celery_worker()`

### Exemplo de Uso

```python
_celery_worker()
```

## Função: `_thread_api()`

**Retorna:** NoReturn

### Exemplo de Uso

```python
resultado = _thread_api()
```

## Função: `_thread_celery()`

**Retorna:** NoReturn

### Exemplo de Uso

```python
resultado = _thread_celery()
```

## Função: `_start_backend()`

### Exemplo de Uso

```python
_start_backend()
```

