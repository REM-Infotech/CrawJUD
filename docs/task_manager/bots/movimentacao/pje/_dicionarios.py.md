# task_manager/bots/movimentacao/pje/_dicionarios.py

## Propósito

Módulo do sistema CrawJUD.

## Dependências Principais

- `__future__`
- `typing`

## Classe: `PJeMovimentacao`

**Herda de:** `TypedDict`

### Atributos

- `NUMERO_PROCESSO` (str)
- `GRAU` (str)
- `REGIAO` (str)

## Classe: `ExpedienteDocumento`

**Herda de:** `TypedDict`

### Atributos

- `expediente` (bool)
- `expedienteAberto` (bool)
- `hasMandadoDevolucaoPendente` (bool)
- `mandadoDistribuido` (bool)

## Classe: `DocumentoPJe`

**Herda de:** `TypedDict`

### Atributos

- `id` (int)
- `idUnicoDocumento` (str)
- `titulo` (str)
- `idTipo` (int)
- `tipo` (str)
- `codigoDocumento` (str)
- `data` (str)
- `documento` (bool)
- `idUsuario` (int)
- `especializacoes` (int)
- `nomeResponsavel` (str)
- `anexos` (list[DocumentoPJe])
- `tipoPolo` (str)
- `participacaoProcesso` (str)
- `favorito` (bool)
- `ativo` (bool)
- `documentoSigiloso` (bool)
- `usuarioInterno` (bool)
- `documentoApreciavel` (bool)
- `instancia` (str)
- `idSignatario` (int)
- `nomeSignatario` (str)
- `expediente` (bool)
- `numeroOrdem` (int)
- `codigoInstancia` (int)
- `pendenciaDocInstanciaOrigem` (bool)
- `papelUsuarioDocumento` (str)
- `infoExpedientes` (ExpedienteDocumento)
- `copia` (bool)
- `permiteCooperacaoJudiciaria` (bool)
- `dataJuntadaFutura` (bool)

