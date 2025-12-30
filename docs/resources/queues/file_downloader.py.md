# resources/queues/file_downloader.py

## Propósito

Gerencie downloads de arquivos em fila com suporte a múltiplas threads.

Este módulo fornece:
- FileDownload: dicionário tipado para tarefas de download de arquivos.
- FileDownloader: classe para gerenciar e executar downloads em fila,
  utilizando uma thread dedicada e suporte a cookies HTTP.

## Dependências Principais

- `__future__`
- `backend.resources.iterators.queues`
- `httpx`
- `pathlib`
- `queue`
- `threading`
- `time`
- `tqdm`
- `traceback`
- `typing`

## Constantes

- `BUFFER_1MB`
- `CHUNK_8MB`

## Classe: `FileDownload`

Defina o dicionário para informações de download de arquivo.

Args:
    link_file (str): URL do arquivo para download.
    file (str): Caminho do arquivo de destino.
    cookies (dict[str, str]): Cookies HTTP para autenticação.

**Herda de:** `TypedDict`

### Atributos

- `link_file` (str)
- `file` (str)
- `cookies` (dict[str, str])

## Classe: `FileDownloader`

Gerencie downloads de arquivos em uma fila usando thread dedicada.

Permite adicionar tarefas de download em uma fila e processa cada
tarefa em uma thread separada, realizando o download dos arquivos
especificados.

### Métodos

#### `__init__()`

Inicialize o gerenciador de downloads e inicie a thread da fila.

**Parâmetros:**

- `self` (Any)

#### `queue_download()`

Consuma a fila de downloads e realize o download dos arquivos.

**Parâmetros:**

- `self` (Any)

#### `__call__()`

Adicione uma nova tarefa de download à fila.

Args:
    file (str): Caminho do arquivo de destino.
    link (str): URL do arquivo para download.
    cookies (dict[str, str]): Cookies HTTP para autenticação.

**Parâmetros:**

- `self` (Any)
- `file` (str)
- `link` (str)
- `cookies` (dict[str, str])

