# api/_forms/head.py

## Propósito

Módulo do sistema CrawJUD.

## Dependências Principais

- `__future__`
- `backend.api.resources`
- `backend.common.exceptions._fatal`
- `backend.models`
- `backend.types_app`
- `base64`
- `flask_jwt_extended`
- `flask_keepass`
- `traceback`
- `typing`

## Classe: `FormBot`

Classe base para formulários de bots.

Gerencia o registro dinâmico de subclasses e fornece métodos utilitários
para carregar formulários, manipular tarefas e converter dados.

### Atributos

- `_subclass` (ClassVar[dict[str, type[Self]]])

### Métodos

#### `load_form()`

Carregue e retorne uma instância do formulário solicitado.

Args:
    cls (type[Self]): Classe do formulário.

Returns:
    Self: Instância do formulário carregado.

**Parâmetros:**

- `cls` (Any)

**Retorna:** Self

#### `handle_task()`

Envie tarefas para execução assíncrona via Celery e notifique o usuário.

Args:
    pid_exec (str): Identificador do processo de execução.

**Parâmetros:**

- `self` (Any)
- `pid_exec` (str)

#### `to_dict()`

Converta os atributos do formulário em um dicionário serializável.

Returns:
    Dict: Dicionário com os dados do formulário.

**Parâmetros:**

- `self` (Any)

**Retorna:** Dict

#### `__init_subclass__()`

Registre automaticamente subclasses para carregamento dinâmico.

Args:
    cls (type[Self]): Subclasse a ser registrada.

**Parâmetros:**

- `cls` (type[Self])

