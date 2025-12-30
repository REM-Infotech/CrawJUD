# task_manager/bots/admin/elaw/download.py

## Propósito

Gerencie downloads de documentos judiciais no sistema ELAW.

Este módulo contém classes e funções para buscar, baixar e renomear
documentos de processos judiciais conforme critérios definidos.

## Dependências Principais

- `backend.common.exceptions`
- `backend.controllers.elaw`
- `backend.resources.elements`
- `os`
- `pathlib`
- `selenium.webdriver.common.by`
- `selenium.webdriver.support`
- `shutil`
- `time`

## Classe: `Download`

Gerencie downloads de documentos do sistema ELAW.

Esta classe executa buscas, downloads e renomeia arquivos
conforme critérios definidos para processos judiciais.

**Herda de:** `ElawBot`

### Métodos

#### `execution()`

Execute o fluxo principal de download dos documentos.

Percorre os processos, executa buscas e gerencia erros.

**Parâmetros:**

- `self` (Any)

#### `queue()`

Handle the download queue processing.

Raises:
    ExecutionError: If an error occurs during queue processing.

**Parâmetros:**

- `self` (Any)

#### `buscar_doc()`

Acesse a página de anexos e a tabela de documentos.

**Parâmetros:**

- `self` (Any)

#### `download_docs()`

Baixe e renomeie documentos conforme termos definidos.

**Parâmetros:**

- `self` (Any)

#### `rename_doc()`

Rename the downloaded document.

Args:
    namefile (str): The new name for the file.

**Parâmetros:**

- `self` (Any)
- `namefile` (str)

