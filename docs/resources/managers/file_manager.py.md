# resources/managers/file_manager.py

## Propósito

Gerenciador de arquivos recebidos para a execução do robô.

## Dependências Principais

- `__future__`
- `backend.config`
- `backend.controllers.head`
- `backend.resources.formatadores`
- `celery`
- `minio.datatypes`
- `pathlib`
- `tqdm`
- `typing`
- `zipfile`

## Classe: `FileManager`

Gerenciador de arquivos recebidos para a execução do robô.

**Herda de:** `MinioClient`

### Atributos

- `celery_app` (Celery)

### Métodos

#### `__init__()`

Inicialize o gerenciador com o bot informado.

Args:
    bot (CrawJUD): Instância do robô principal.

**Parâmetros:**

- `self` (Any)
- `bot` (CrawJUD)

#### `__filter_files()`

**Parâmetros:**

- `self` (Any)
- `item` (Object)

**Retorna:** bool

#### `download_files()`

Baixe arquivos do Minio para o diretório de saída do robô.

**Parâmetros:**

- `self` (Any)

#### `upload_file()`

Gere e envie arquivo zip ao Minio, retornando URL.

Returns:
    str: URL para download do arquivo zip enviado.

**Parâmetros:**

- `self` (Any)

**Retorna:** str

#### `__zip_result()`

**Parâmetros:**

- `self` (Any)

**Retorna:** Path

