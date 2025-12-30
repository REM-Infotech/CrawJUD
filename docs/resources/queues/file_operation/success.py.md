# resources/queues/file_operation/success.py

## Propósito

Operações de planilhas.

## Dependências Principais

- `__future__`
- `backend.controllers.head`
- `backend.interfaces`
- `backend.resources.iterators.queues`
- `backend.resources.queues.file_operation.main`
- `datetime`
- `pandas`
- `queue`
- `threading`
- `typing`

## Constantes

- `DATASAVE`

## Classe: `SaveSuccess`

Controle da Queue de salvamento de sucessos.

**Herda de:** `FileOperator`

### Atributos

- `bot` (CrawJUD)

### Métodos

#### `__init__()`

Instancia da queue de salvamento de erros.

**Parâmetros:**

- `self` (Any)
- `bot` (CrawJUD)

#### `__call__()`

Adicione dados de sucesso à fila para processamento assíncrono.

Args:
    worksheet (str): Nome da planilha de destino.
    data_save (str): Dados a serem salvos na planilha.

**Parâmetros:**

- `self` (Any)
- `worksheet` (str)
- `data_save` (str)

#### `save_success()`

Salve dados de sucesso em arquivo Excel de forma assíncrona.

**Parâmetros:**

- `self` (Any)

**Retorna:** NoReturn

