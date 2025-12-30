# extensions/__init__.py

## Propósito

Extensões do App.

## Dependências Principais

- `__future__`
- `backend.extensions._minio`
- `celery`
- `flask_jwt_extended`
- `flask_mail`
- `flask_socketio`
- `passlib.context`
- `pathlib`
- `socketio.redis_manager`
- `typing`

## Função: `start_extensions()`

Inicializa as extensões do Flask.

**Parâmetros:**

- `app` (Flask)

**Retorna:** Flask

### Exemplo de Uso

```python
resultado = start_extensions(app)
```

