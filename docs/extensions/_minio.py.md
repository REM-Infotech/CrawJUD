# extensions/_minio.py

## Propósito

Módulo do sistema CrawJUD.

## Dependências Principais

- `__future__`
- `backend.types_app`
- `collections.abc`
- `dotenv`
- `flask`
- `functools`
- `minio`
- `minio.credentials.providers`
- `typing`

## Classe: `Minio`

**Herda de:** `MinioClient`

### Atributos

- `flask_app` (Flask)

### Métodos

#### `__init__()`

**Parâmetros:**

- `self` (Any)
- `app` (Flask | None)

#### `init_app()`

Inicializa a extensão com a aplicação Flask.

**Parâmetros:**

- `self` (Any)
- `app` (Flask)

#### `decorate_functions()`

**Parâmetros:**

- `self` (Any)

#### `wrapper()`

**Parâmetros:**

- `cls` (Any)
- `func` (Callable[P, T])

**Retorna:** Callable[P, T]

