# api/routes/api/_auth.py

## Propósito

Módulo de controle das rotas de autenticação da API.

## Dependências Principais

- `__future__`
- `backend.api.routes._blueprints`
- `backend.models`
- `backend.utilities`
- `contextlib`
- `flask_jwt_extended`
- `flask_sqlalchemy`
- `traceback`
- `typing`
- `werkzeug.exceptions`

## Função: `login()`

Rota de autenticação da api.

Returns:
    Response: Response da autenticação

**Retorna:** Response

### Exemplo de Uso

```python
resultado = login()
```

## Função: `logout()`

Rota de logout.

Returns:
    Response: Response do logout.

**Retorna:** Response

### Exemplo de Uso

```python
resultado = logout()
```

