# task_manager/extensions/__init__.py

## Propósito

Extensões do App.

## Dependências Principais

- `__future__`
- `backend.task_manager.base`
- `backend.task_manager.constants`
- `contextlib`
- `flask`
- `flask_mail`
- `flask_sqlalchemy`
- `passlib.context`
- `typing`

## Função: `start_extensions()`

Inicializa as extensões do Flask.

**Parâmetros:**

- `app` (Flask)

### Exemplo de Uso

```python
start_extensions(app)
```

