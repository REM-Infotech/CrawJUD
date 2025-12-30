# resources/queues/file_operation/error.py

## Propósito

Gerencia fila e salvamento assíncrono de erros em arquivos Excel.

## Dependências Principais

- `__future__`
- `backend.controllers.head`
- `backend.resources.iterators.queues`
- `backend.resources.queues.file_operation.main`
- `backend.types_app`
- `datetime`
- `pandas`
- `queue`
- `threading`
- `typing`

## Constantes

- `DATASAVE`

## Classe: `SaveError`

Controle da Queue de salvamento de erros.

**Herda de:** `FileOperator`

### Métodos

#### `__init__()`

Instancia da queue de salvamento de erros.

**Parâmetros:**

- `self` (Any)
- `bot` (CrawJUD)

#### `__call__()`

Adiciona dados de erro à fila para salvamento assíncrono.

Args:
    worksheet (str): Nome da planilha de destino.
    data_save (list[Dict]): Lista de dados de erro a serem salvos.

**Parâmetros:**

- `self` (Any)
- `worksheet` (str)
- `data_save` (list[Dict] | None)

#### `save_error()`

Salve erros da fila em arquivo Excel de forma assíncrona.

**Parâmetros:**

- `self` (Any)

**Retorna:** NoReturn

