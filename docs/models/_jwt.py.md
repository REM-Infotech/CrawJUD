# models/_jwt.py

## Propósito

Module for user-related models and authentication utilities.

## Dependências Principais

- `__future__`
- `_users`
- `backend.extensions`
- `backend.types_app`
- `contextlib`
- `datetime`
- `flask_jwt_extended`
- `sqlalchemy`
- `sqlalchemy.orm`
- `typing`

## Classe: `TokenBlocklist`

Database model for token blocklist.

**Herda de:** `db.Model`

### Atributos

- `Id` (int)
- `jti` (str)
- `type` (str)
- `user` (Mapped[User])

## Função: `user_identity_lookup()`

Get the user's identity.

Returns:
    int: The user's ID.

**Parâmetros:**

- `usr_id` (int)

**Retorna:** int

### Exemplo de Uso

```python
resultado = user_identity_lookup(usr_id)
```

## Função: `check_if_token_revoked()`

Check if the token is in the blocklist.

Returns:
    bool: True if the token is revoked, False otherwise.

**Retorna:** bool

### Exemplo de Uso

```python
resultado = check_if_token_revoked()
```

## Função: `user_lookup_callback()`

Get the user from the JWT data.

Returns:
    User | None: The user object or None if not found.

**Retorna:** User | None

### Exemplo de Uso

```python
resultado = user_lookup_callback()
```

