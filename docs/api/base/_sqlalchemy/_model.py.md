# api/base/_sqlalchemy/_model.py

## Propósito

Módulo do sistema CrawJUD.

## Dependências Principais

- `__future__`
- `_query`
- `backend.api.resources`
- `backend.types_app`
- `contextlib`
- `flask`
- `flask_sqlalchemy`
- `flask_sqlalchemy.model`
- `typing`

## Classe: `FSAProperty`

### Atributos

- `fsa_instante` (SQLAlchemy)

### Métodos

#### `__set__()`

**Parâmetros:**

- `self` (Any)

#### `__get__()`

**Parâmetros:**

- `self` (Any)

**Retorna:** SQLAlchemy

## Classe: `FSATableName`

### Atributos

- `_tablename` (ClassVar[str])

### Métodos

#### `__set__()`

**Parâmetros:**

- `self` (Any)

#### `__get__()`

**Parâmetros:**

- `self` (Any)
- `cls` (Model | None)

**Retorna:** str

## Classe: `Model`

**Herda de:** `FSA_Model`

### Atributos

- `query` (ClassVar[Query[Self]])
- `__fsa__` (ClassVar[SQLAlchemy])
- `__tablename__` (ClassVar[str])

### Métodos

#### `to_dict()`

**Parâmetros:**

- `self` (Any)

**Retorna:** dict

