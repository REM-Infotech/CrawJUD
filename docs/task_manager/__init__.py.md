# task_manager/__init__.py

## Propósito

CrawJUD - Sistema de Automação Jurídica.

## Dependências Principais

- `__future__`
- `backend`
- `backend.config`
- `backend.task_manager`
- `backend.task_manager.base`
- `celery`
- `flask`
- `typing`

## Função: `make_celery()`

Create and configure a Celery instance with Quart application context.

Returns:
    Celery: Configured Celery instance.

**Parâmetros:**

- `app` (Flask)

**Retorna:** Celery

### Exemplo de Uso

```python
resultado = make_celery(app)
```

