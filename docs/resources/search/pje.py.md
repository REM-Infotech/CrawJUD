# resources/search/pje.py

## Propósito

Implemente buscas de processos no sistema PJe.

Este módulo contém classes e funções para consultar processos
no sistema PJe utilizando um cliente HTTP.

## Dependências Principais

- `__future__`
- `backend.controllers`
- `backend.interfaces`
- `backend.interfaces.pje`
- `backend.resources.elements`
- `backend.resources.search.main`
- `backend.task_manager.constants`
- `contextlib`
- `httpx`
- `typing`

## Classe: `_ResponseDadosBasicos`

**Herda de:** `TypedDict`

### Atributos

- `id` (int)
- `numeroIdentificacaoJustica` (int)
- `numero` (str)
- `classe` (str)
- `codigoOrgaoJulgador` (int)
- `juizoDigital` (bool)

## Classe: `PjeSeach`

Implemente buscas de processos no sistema PJe.

Esta classe herda de SearchBot e executa consultas
utilizando um cliente HTTP para obter dados de processos.

**Herda de:** `SearchBot`

### Atributos

- `bot` (PJeBot)

### Métodos

#### `regiao()`

**Parâmetros:**

- `self` (Any)

**Retorna:** str

#### `is_grau_list()`

**Parâmetros:**

- `self` (Any)

**Retorna:** bool

#### `__call__()`

Realize a busca de um processo no sistema PJe.

Args:
    data (BotData): Dados do processo a serem consultados.
    row (int): Índice da linha do processo na planilha de entrada.
    client (Client): Instância do cliente HTTP
        para requisições ao sistema PJe.
    regiao (str):regiao

Returns:
    (DictResults | Literal["Nenhum processo encontrado"]): Resultado da
        busca do processo ou mensagem indicando
        que nenhum processo foi encontrado.

**Parâmetros:**

- `self` (Any)
- `data` (BotData)
- `row` (int)
- `client` (Client)

**Retorna:** DictResults | None

#### `_format_response_pje()`

**Parâmetros:**

- `self` (Any)
- `response` (Response)

**Retorna:** _ResponseDadosBasicos

#### `_print_processo_nao_encontrado()`

**Parâmetros:**

- `self` (Any)
- `row` (int)

