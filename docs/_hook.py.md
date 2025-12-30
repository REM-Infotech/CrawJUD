# _hook.py

## Propósito

Módulo do sistema CrawJUD.

## Dependências Principais

- `__future__`
- `importlib.abc`
- `importlib.util`
- `json`
- `packaging.version`
- `pathlib`
- `sys`
- `types`
- `typing`
- `weakref`

## Classe: `Legacy`

**Herda de:** `importlib.abc.SourceLoader`

### Métodos

#### `get_data()`

**Parâmetros:**

- `self` (Any)
- `path` (str)

**Retorna:** str

#### `get_filename()`

**Parâmetros:**

- `self` (Any)
- `fullname` (str)

**Retorna:** str

#### `exec_module()`

**Parâmetros:**

- `self` (Any)
- `module` (ModuleType)

#### `safe_ref()`

Retorne uma referência fraca para o alvo fornecido.

Args:
    target (MyAny): Objeto alvo para criar referência fraca.

Returns:
    MyAny: Referência fraca ao objeto alvo.

**Parâmetros:**

- `self` (Any)
- `target` (MyAny)

**Retorna:** MyAny

## Classe: `JSONLoader`

**Herda de:** `importlib.abc.SourceLoader`

### Métodos

#### `get_data()`

**Parâmetros:**

- `self` (Any)
- `path` (str)

**Retorna:** str

#### `get_filename()`

**Parâmetros:**

- `self` (Any)
- `fullname` (str)

**Retorna:** str

#### `exec_module()`

**Parâmetros:**

- `self` (Any)
- `module` (ModuleType)

## Classe: `JSONFinder`

**Herda de:** `importlib.abc.MetaPathFinder`

### Métodos

#### `find_spec()`

**Parâmetros:**

- `self` (Any)
- `fullname` (str)
- `_path` (str)
- `_target` (MyAny)

**Retorna:** ModuleType | None

#### `guess()`

**Parâmetros:**

- `self` (Any)
- `path` (Path)

**Retorna:** bool

