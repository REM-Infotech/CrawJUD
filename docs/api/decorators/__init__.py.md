# api/decorators/__init__.py

## Propósito

Decoradores do app.

## Dependências Principais

- `__future__`
- `backend.api.decorators._api`
- `collections.abc`
- `flask_jwt_extended`
- `functools`
- `typing`

## Constantes

- `P`

## Função: `jwt_sio_required()`

**Parâmetros:**

- `fn` (Callable[P, T])

**Retorna:** Callable[P, T]

### Exemplo de Uso

```python
resultado = jwt_sio_required(fn)
```

