# task_manager/bots/capa/pje/_audiencias.py

## Propósito

Módulo do sistema CrawJUD.

## Dependências Principais

- `__future__`
- `backend.resources.elements`
- `contextlib`
- `httpx`
- `typing`

## Classe: `AudienciasProcessos`

Defina os campos das audiências do processo no padrão PJe.

Args:
    ID_PJE (int): Identificador único do processo no PJE.
    NUMERO_PROCESSO (str): Número do processo judicial.
    TIPO_AUDIENCIA (str): Tipo da audiência.
    MODO_AUDIENCIA (str): Modo de realização da audiência.
    STATUS (str): Status da audiência.
    DATA_INICIO (str): Data de início da audiência.
    DATA_FIM (str): Data de término da audiência.
    DATA_MARCACAO (str): Data de marcação da audiência.

**Herda de:** `TypedDict`

### Atributos

- `ID_PJE` (int)
- `NUMERO_PROCESSO` (str)
- `TIPO_AUDIENCIA` (str)
- `MODO_AUDIENCIA` (str)
- `STATUS` (str)
- `DATA_INICIO` (str)
- `DATA_FIM` (str)
- `DATA_MARCACAO` (str)

## Classe: `InformacoesAudiencias`

### Métodos

#### `audiencias()`

**Parâmetros:**

- `cls` (Any)
- `regiao` (str)
- `id_processo` (str)
- `cliente` (Client)

#### `_formata_audiencias()`

**Parâmetros:**

- `cls` (Any)
- `processo` (str)
- `data_audiencia` (list[dict])

**Retorna:** list[AudienciasProcessos]

