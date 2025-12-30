# api/routes/__init__.py

## Propósito

Gerencie rotas principais e registro de blueprints da aplicação.

Este módulo define rotas básicas e integra blueprints de autenticação e bots.

## Dependências Principais

- `__future__`
- `_blueprints`
- `backend.api`
- `flask`
- `flask_socketio`
- `typing`

## Função: `register_routes()`

**Parâmetros:**

- `app` (Flask)

### Exemplo de Uso

```python
register_routes(app)
```

## Função: `apply_cors()`

**Parâmetros:**

- `response` (Response)

**Retorna:** Response

### Exemplo de Uso

```python
resultado = apply_cors(response)
```

