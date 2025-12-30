# api/decorators/_api.py

## Propósito

Módulo do decorator CrossDomain.

## Dependências Principais

- `__future__`
- `backend.types_app`
- `collections.abc`
- `datetime`
- `flask`
- `functools`
- `typing`

## Constantes

- `MAX_AGE`

## Classe: `CrossDomain`

Adicione cabeçalhos CORS às respostas HTTP para permitir requisições cross-origin.

Esta classe fornece métodos utilitários para normalizar métodos, cabeçalhos, origens
e tempo de cache, além de um decorador para aplicar as regras CORS em rotas HTTP.

### Métodos

#### `__init__()`

Inicializa o objeto CrossDomain com configurações de CORS personalizadas.

Args:
    origin (str | None): Origem permitida para requisições CORS.
    methods (Methods | None): Métodos HTTP permitidos.
    headers (list[str] | None): Lista de cabeçalhos permitidos.
    max_age (int): Tempo máximo de cache dos cabeçalhos CORS em segundos.
    attach_to_all (bool): Se deve anexar cabeçalhos a todas as respostas.
    automatic_options (bool): Se deve gerar resposta automática para OPTIONS.

**Parâmetros:**

- `self` (Any)
- `origin` (str | None)
- `methods` (list[Methods] | None)
- `headers` (list[str] | None)
- `_max_age` (int)

#### `__call__()`

Adiciona cabeçalhos CORS à resposta HTTP.

Args:
    wrapped_function (Callable[P, T]): Função a ser decorada para receber os
        cabeçalhos CORS.
    origin (str | None): Origem permitida para CORS.
    methods (list[str] | None): Métodos HTTP permitidos.
    headers (list[str] | None): Cabeçalhos permitidos.
    max_age (int): Tempo máximo de cache dos cabeçalhos CORS.
    attach_to_all (bool): Se deve anexar cabeçalhos a todas respostas.
    automatic_options (bool): Se deve gerar resposta automática para OPTIONS.

Returns:
    Callable: Decorador que adiciona cabeçalhos CORS à resposta.

**Parâmetros:**

- `self` (Any)
- `wrapped_function` (Callable[P, T])

**Retorna:** Callable[P, Response]

#### `_normalize_methods()`

Normaliza os métodos HTTP para cabeçalho CORS.

Args:
    methods (list[str] | None): Lista de métodos HTTP ou None.

Returns:
    str | None: Métodos HTTP normalizados em string ou None.

**Parâmetros:**

- `cls` (Any)
- `methods` (list[Methods] | None)

**Retorna:** str | None

#### `_normalize_headers()`

Normaliza os cabeçalhos para CORS.

Args:
    headers (list[str] | None): Lista de cabeçalhos HTTP ou None.

Returns:
    str | None: Cabeçalhos normalizados em string ou None.

**Parâmetros:**

- `cls` (Any)
- `headers` (list[str] | None)

**Retorna:** str | None

#### `_normalize_origin()`

Normaliza a origem para CORS.

Args:
    origin (str | None): Origem permitida para CORS.

Returns:
    str | None: Origem normalizada como string ou None.

**Parâmetros:**

- `cls` (Any)
- `origin` (str | None)

**Retorna:** str | None

#### `_normalize_max_age()`

Normaliza o tempo máximo de cache para CORS.

Args:
    max_age (int | timedelta): Tempo máximo de cache em segundos ou timedelta.

Returns:
    int: Tempo máximo de cache em segundos.

**Parâmetros:**

- `cls` (Any)
- `max_age` (int | timedelta)

**Retorna:** int

#### `_get_methods()`

Obtém os métodos permitidos para CORS.

Returns:
    str: Métodos HTTP permitidos, formatados para cabeçalho CORS.

**Parâmetros:**

- `cls` (Any)
- `normalized_methods` (str | None)

**Retorna:** str

#### `_handle_options()`

Gera resposta para método OPTIONS.

Returns:
    Response: Resposta padrão para o método OPTIONS.

**Parâmetros:**

- `cls` (Any)

**Retorna:** Response

#### `_handle_request()`

Processa requisição com verificação de XSRF.

Returns:
    Response: Resposta HTTP gerada após o processamento da requisição.

**Parâmetros:**

- `self` (Any)
- `function` (Callable)

**Retorna:** Response

#### `_set_cors_headers()`

Define os cabeçalhos CORS na resposta.

**Parâmetros:**

- `self` (Any)
- `resp` (Response)
- `normalized_origin` (str | None)
- `normalized_methods` (str | None)
- `normalized_headers` (str | None)
- `normalized_max_age` (int)

