# task_manager/bots/admin/elaw/solicita_pagamento/custas.py

## Propósito

Gerencie o pagamento de custas judiciais no sistema Elaw.

Este módulo contém classes e funções para automatizar o fluxo de
pagamento de custas judiciais, incluindo inicialização, validação,
informação de valores, anexos e dados do favorecido.

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

- `TIPO_DOCUMENTO`
- `FAVORECIDO`
- `CENTRO_CUSTAS`
- `CONTA_DEBITO`

## Classe: `PgtoCustas`

Gerencie o pagamento de custas judiciais no sistema Elaw.

Esta classe integra métodos para informar valores, anexar arquivos,
preencher dados do favorecido, centro de custas e conta de débito.

**Herda de:** `Inicializacao`, `Inputs`, `Seletores`, `Validador`

### Métodos

#### `custas()`

Execute o pagamento das custas judiciais no Elaw.

Esta função realiza o fluxo completo de pagamento das custas,
incluindo valor, anexos, favorecido, centro de custas e conta.

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

