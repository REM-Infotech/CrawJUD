# task_manager/bots/capa/projudi/primeira.py

## Propósito

Automações para processos judiciais no Projudi.

## Dependências Principais

- `__future__`
- `backend.controllers.projudi`
- `backend.interfaces.projudi`
- `backend.resources.elements`
- `backend.task_manager.constants`
- `backend.types_app`
- `bs4`
- `selenium.webdriver.common.by`
- `selenium.webdriver.support`
- `typing`

## Classe: `PrimeiraInstancia`

Automações para processos de 1ª instância no Projudi.

Esta classe herda de ProjudiBot e contém métodos para extrair
informações gerais, processuais e das partes de processos judiciais
no sistema Projudi.

**Herda de:** `ProjudiBot`

### Métodos

#### `_informacoes_gerais_primeiro_grau()`

**Parâmetros:**

- `self` (Any)

#### `_info_processual_primeiro_grau()`

**Parâmetros:**

- `self` (Any)

**Retorna:** dict[str, str]

#### `_partes_primeiro_grau()`

**Parâmetros:**

- `self` (Any)
- `numero_processo` (str)

**Retorna:** tuple[list[PartesProjudiDict], list[RepresentantesProjudiDict]]

#### `_partes_extract_primeiro_grau()`

Extraia informações das partes do processo na tabela do Projudi.

Args:
    html (str): HTML da página contendo a tabela de partes.
    processo(str): Numero processo

Returns:
    tuple: advogados e partes

**Parâmetros:**

- `self` (Any)
- `html` (str)
- `processo` (str)

**Retorna:** tuple[list[PartesProjudiDict], list[RepresentantesProjudiDict]]

