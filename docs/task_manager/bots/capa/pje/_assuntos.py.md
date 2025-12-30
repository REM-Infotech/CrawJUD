# task_manager/bots/capa/pje/_assuntos.py

## Propósito

Módulo do sistema CrawJUD.

## Dependências Principais

- `__future__`
- `backend.resources.elements`
- `contextlib`
- `httpx`
- `typing`

## Classe: `Assuntos`

Defina os campos dos assuntos do processo judicial no padrão PJe.

Args:
    ID_PJE (int): Identificador único do processo no PJE.
    PROCESSO (str): Número do processo judicial.
    ASSUNTO_COMPLETO (str): Descrição completa do assunto.
    ASSUNTO_RESUMIDO (str): Descrição resumida do assunto.

Returns:
    Assuntos: Dicionário tipado com os dados dos assuntos.

**Herda de:** `TypedDict`

### Atributos

- `ID_PJE` (int)
- `PROCESSO` (str)
- `ASSUNTO_COMPLETO` (str)
- `ASSUNTO_RESUMIDO` (str)

## Classe: `AssuntosPJe`

### Métodos

#### `assuntos()`

**Parâmetros:**

- `cls` (Any)
- `cliente` (Client)
- `regiao` (str)
- `id_processo` (str)

**Retorna:** list[Assuntos]

