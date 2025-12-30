# models/__init__.py

## Propósito

Módulo de gestão de Models do banco de dados.

## Dependências Principais

- `__future__`
- `_jwt`
- `backend.interfaces`
- `backend.models._bot`
- `backend.types_app`
- `flask`
- `flask_keepass`
- `pathlib`
- `typing`
- `uuid`

## Função: `init_database()`

Inicializa o banco de dados.

**Parâmetros:**

- `app` (Flask)

### Exemplo de Uso

```python
init_database(app)
```

## Função: `create_bots()`

**Parâmetros:**

- `app` (Flask)

### Exemplo de Uso

```python
create_bots(app)
```

## Função: `load_credentials()`

**Parâmetros:**

- `app` (Flask)

### Exemplo de Uso

```python
load_credentials(app)
```

## Função: `import_users()`

**Parâmetros:**

- `app` (Flask)

### Exemplo de Uso

```python
import_users(app)
```

