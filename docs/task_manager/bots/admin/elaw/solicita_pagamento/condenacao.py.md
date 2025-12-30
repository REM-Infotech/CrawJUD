# task_manager/bots/admin/elaw/solicita_pagamento/condenacao.py

## Propósito

Define bot para solicitação de pagamento de condenação no Elaw.

## Dependências Principais

- `__future__`
- `backend.common.raises`
- `backend.interfaces.elaw.main`
- `backend.resources.elements.elaw`
- `inicializacao`
- `inputs`
- `seletores`
- `traceback`
- `validacao`

## Constantes

- `CNPJ_TJAM`
- `CONTA_DEBITO`
- `PGTO_BOLETO`
- `CENTRO_CUSTAS`
- `TIPO_DOCUMENTO`

## Classe: `PgtoCondenacao`

Gerencia solicitação de pagamento de condenação no Elaw.

**Herda de:** `Inicializacao`, `Inputs`, `Seletores`, `Validador`

### Métodos

#### `condenacao()`

Execute a solicitação de pagamento de condenação no Elaw.

**Parâmetros:**

- `self` (Any)

#### `__envia_arquivos()`

Envie arquivos necessários para o pagamento da condenação.

Esta função faz o upload dos arquivos de guia de pagamento e
cálculo, caso existam, utilizando os elementos da interface
do sistema Elaw.

**Parâmetros:**

- `self` (Any)

#### `__informa_favorecido()`

Informe o favorecido no campo do formulário.

Preencha o campo de favorecido com o CNPJ informado ou padrão.

**Parâmetros:**

- `self` (Any)

#### `__informa_centro_custa()`

Informe o centro de custas no campo correspondente.

Esta função preenche o campo de centro de custas utilizando
os dados fornecidos pelo bot ou o valor padrão.

**Parâmetros:**

- `self` (Any)

#### `__conta_debito()`

Informe a conta para débito no campo correspondente.

Esta função seleciona a conta de débito no formulário do sistema
Elaw, utilizando os dados fornecidos pelo bot ou o valor padrão.

**Parâmetros:**

- `self` (Any)

