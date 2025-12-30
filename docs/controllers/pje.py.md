# controllers/pje.py

## Propósito

Módulo para a classe de controle dos robôs PJe.

## Dependências Principais

- `__future__`
- `backend.controllers.head`
- `backend.resources`
- `backend.resources.auth.pje`
- `backend.resources.queues.file_downloader`
- `backend.resources.search.pje`
- `backend.types_app`
- `backend.types_app.bot`
- `dotenv`
- `typing`

## Classe: `PJeBot`

Classe de controle para robôs do PJe.

**Herda de:** `CrawJUD`

### Atributos

- `_regiao` (ClassVar[int])
- `_is_grau_list` (ClassVar[bool])
- `download_file` (FileDownloader)
- `posicoes_processos` (ClassVar[Dict])
- `auth` (AutenticadorPJe)

### Métodos

#### `__init__()`

Inicialize o robô PJe com autenticação e busca.

**Parâmetros:**

- `self` (Any)

#### `list_posicao_processo()`

Liste as posições dos processos cadastrados.

Returns:
    Dict[str, int]: Dicionário com posições dos processos.

**Parâmetros:**

- `self` (Any)

**Retorna:** Dict[ProcessoCNJ, int]

#### `data_regiao()`

Obtenha a lista de dados das regiões cadastradas.

Returns:
    list[BotData]: Lista de dados das regiões.

**Parâmetros:**

- `self` (Any)

**Retorna:** list[BotData]

#### `data_regiao()`

Defina a lista de dados das regiões cadastradas.

Args:
    _data_regiao (list[BotData]): Lista de dados das regiões.

**Parâmetros:**

- `self` (Any)
- `_data_regiao` (list[BotData])

#### `regiao()`

Obtenha a região cadastrada.

Returns:
    str: Região cadastrada.

**Parâmetros:**

- `self` (Any)

**Retorna:** str

#### `regiao()`

Defina a região cadastrada.

Args:
    _regiao (str): Região a ser definida.

**Parâmetros:**

- `self` (Any)
- `_regiao` (str)

#### `regioes()`

Lista as regiões disponíveis do PJe.

Returns:
    RegioesIterator: Iterador das regiões do PJe.

**Parâmetros:**

- `self` (Any)

**Retorna:** RegioesIterator

