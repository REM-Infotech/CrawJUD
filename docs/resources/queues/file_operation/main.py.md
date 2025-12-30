# resources/queues/file_operation/main.py

## Propósito

Gerencie operações de leitura e escrita em arquivos Excel.

Este módulo fornece a classe FileOperator para manipular planilhas.

## Dependências Principais

- `__future__`
- `backend.interfaces`
- `contextlib`
- `openpyxl`
- `pandas`
- `pathlib`
- `typing`

## Classe: `FileOperator`

Gerencie operações de leitura e escrita em arquivos Excel.

Esta classe oferece métodos para carregar, criar e salvar dados
em arquivos Excel, facilitando a manipulação de planilhas.

### Métodos

#### `load_writer()`

Carregue ou crie um ExcelWriter para o arquivo informado.

Args:
    arquivo_xlsx (Path): Caminho do arquivo Excel.

Returns:
    ExcelWriter: Objeto para manipulação do arquivo Excel.

**Parâmetros:**

- `cls` (Any)
- `arquivo_xlsx` (Path)

**Retorna:** ExcelWriter

#### `save_file()`

Salve dados em uma planilha Excel existente ou nova.

Args:
    data (DataSave): Dados e nome da worksheet.
    arquivo_xlsx (Path): Caminho do arquivo Excel.

**Parâmetros:**

- `self` (Any)
- `data` (DataSave)
- `arquivo_xlsx` (Path)

