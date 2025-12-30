# interfaces/elaw/pagamentos.py

## Propósito

Defina interfaces de dados para pagamentos do sistema Elaw.

Este módulo contém a classe CondenacaoData para estruturar
informações de pagamentos e condenações processuais.

## Dependências Principais

- `__future__`
- `backend.types_app`
- `backend.types_app.bot`
- `typing`

## Classe: `ISolicitacaoPagamentos`

Defina interface para solicitações de pagamentos Elaw.

Estruture chamadas para processar pagamentos no sistema.

**Herda de:** `Protocol[P, T]`

### Métodos

#### `__init__()`

Inicialize a interface com o bot do Elaw.

Args:
    bot (T): Instância do bot para processar pagamentos.

**Parâmetros:**

- `self` (Any)
- `bot` (T)

#### `__call__()`

Execute a solicitação de pagamento Elaw.

**Parâmetros:**

- `self` (Any)

## Classe: `CondenacaoDataType`

Estruture dados de condenação e pagamento do Elaw.

Esta classe organiza informações de pagamentos
processuais, como valores, documentos e partes.

**Herda de:** `TypedDict`

### Atributos

- `NUMERO_PROCESSO` (ProcessoCNJ)
- `DESC_PAGAMENTO` (str)
- `VALOR_GUIA` (str)
- `DATA_LANCAMENTO` (str)
- `TIPO_PAGAMENTO` (str)
- `SOLICITANTE` (str)
- `TIPO_CONDENACAO` (str)
- `COD_BARRAS` (str)
- `DOC_GUIA` (str)
- `DOC_CALCULO` (str)
- `LOCALIZACAO` (str)
- `CNPJ_FAVORECIDO` (str)
- `FORMA_PAGAMENTO` (str)
- `CENTRO_CUSTAS` (str)
- `CONTA_DEBITO` (str)

## Classe: `CustasDataType`

Estruture dados de custas processuais do sistema Elaw.

Organize informações de guias, valores e partes envolvidas.

**Herda de:** `TypedDict`

### Atributos

- `NUMERO_PROCESSO` (ProcessoCNJ)
- `TIPO_GUIA` (str)
- `VALOR_GUIA` (str)
- `DATA_LANCAMENTO` (str)
- `TIPO_PAGAMENTO` (str)
- `SOLICITANTE` (str)
- `DESC_PAGAMENTO` (str)
- `COD_BARRAS` (str)
- `DOC_GUIA` (str)
- `LOCALIZACAO` (str)
- `CNPJ_FAVORECIDO` (str)
- `FORMA_PAGAMENTO` (str)
- `CENTRO_CUSTAS` (str)
- `CONTA_DEBITO` (str)

