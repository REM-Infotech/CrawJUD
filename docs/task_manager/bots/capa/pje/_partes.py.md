# task_manager/bots/capa/pje/\_partes.py

## Propósito

Módulo do sistema CrawJUD.

## Dependências Principais

- `__future__`
- `backend.resources.elements`
- `contextlib`
- `httpx`
- `typing`

## Classe: `PartePJe`

Defina os campos das partes do processo judicial no padrão PJe.

Args:
ID_PJE (int): Identificador único do processo no PJE.
NOME (str): Nome da parte.
DOCUMENTO (str): Documento da parte.
TIPO_DOCUMENTO (str): Tipo do documento.
TIPO_PARTE (str): Tipo da parte (autor/réu).
TIPO_PESSOA (str): Tipo da pessoa (física/jurídica).
PROCESSO (str): Número do processo.
POLO (str): Polo da parte (ativo/passivo).
PARTE_PRINCIPAL (bool): Indica se é parte principal.

**Herda de:** `TypedDict`

### Atributos

- `ID_PJE` (int)
- `NOME` (str)
- `DOCUMENTO` (str)
- `TIPO_DOCUMENTO` (str)
- `TIPO_PARTE` (str)
- `TIPO_PESSOA` (str)
- `PROCESSO` (str)
- `POLO` (str)
- `PARTE_PRINCIPAL` (bool)

## Classe: `Representantes`

Defina os campos dos representantes das partes no padrão PJe.

Args:
ID_PJE (int): Identificador único do processo no PJE.
NOME (str): Nome do representante.
DOCUMENTO (str): Documento do representante.
TIPO_DOCUMENTO (str): Tipo do documento.
REPRESENTADO (str): Nome da parte representada.
TIPO_PARTE (str): Tipo da parte representada.
TIPO_PESSOA (str): Tipo da pessoa (física/jurídica).
PROCESSO (str): Número do processo.
POLO (str): Polo da parte (ativo/passivo).
OAB (str): Número da OAB do representante.
EMAILS (str): E-mails do representante.
TELEFONE (str): Telefone do representante.

Returns:
Representantes: Dicionário tipado com dados do representante.

**Herda de:** `TypedDict`

### Atributos

- `ID_PJE` (int)
- `NOME` (str)
- `DOCUMENTO` (str)
- `TIPO_DOCUMENTO` (str)
- `REPRESENTADO` (str)
- `TIPO_PARTE` (str)
- `TIPO_PESSOA` (str)
- `PROCESSO` (str)
- `POLO` (str)
- `OAB` (str)
- `EMAILS` (str)
- `TELEFONE` (str)

## Classe: `PartesPJe`

### Métodos

#### `__formata_numero_representante()`

**Parâmetros:**

- `representante` (AnyType)

**Retorna:** str

#### `partes()`

**Parâmetros:**

- `cls` (Any)
- `cliente` (Client)
- `regiao` (str)
- `id_processo` (str)

#### `formata_partes()`

**Parâmetros:**

- `cls` (Any)
- `request_partes` (list[dict[str, str]])

#### `formata_representantes()`

**Parâmetros:**

- `cls` (Any)
- `unformatted` (list[dict[str, str]])
