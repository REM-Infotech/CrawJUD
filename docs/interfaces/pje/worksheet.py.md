# interfaces/pje/worksheet.py

## Propósito

Dicionários para salvamento em planilha.

## Dependências Principais

- `__future__`
- `datetime`
- `typing`

## Classe: `CapaPJe`

Defina os campos da capa do processo no padrão PJe.

Args:
    ID_PJE (int): Identificador único do processo no PJE.
    LINK_CONSULTA (str): Link para consulta do processo.
    NUMERO_PROCESSO (str): Número do processo judicial.
    CLASSE (str): Classe do processo.
    SIGLA_CLASSE (str): Sigla da classe do processo.
    ORGAO_JULGADOR (str): Nome do órgão julgador.
    SIGLA_ORGAO_JULGADOR (str): Sigla do órgão julgador.
    DATA_DISTRIBUICAO (datetime): Data de distribuição.
    STATUS_PROCESSO (str): Status do processo.
    SEGREDO_JUSTICA (str): Indica segredo de justiça.

**Herda de:** `TypedDict`

### Atributos

- `ID_PJE` (int)
- `LINK_CONSULTA` (str)
- `NUMERO_PROCESSO` (str)
- `CLASSE` (str)
- `SIGLA_CLASSE` (str)
- `ORGAO_JULGADOR` (str)
- `SIGLA_ORGAO_JULGADOR` (str)
- `DATA_DISTRIBUICAO` (datetime)
- `STATUS_PROCESSO` (str)
- `SEGREDO_JUSTICA` (str)

