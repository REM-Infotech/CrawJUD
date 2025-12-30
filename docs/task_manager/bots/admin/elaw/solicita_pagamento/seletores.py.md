# task_manager/bots/admin/elaw/solicita_pagamento/seletores.py

## Propósito

Gerencie seletores e ações para o fluxo de solicitação Elaw.

Este módulo contém a classe Seletores, responsável por manipular
elementos e ações na tela de solicitação de pagamento do Elaw.

## Dependências Principais

- `__future__`
- `backend.resources.driver`
- `backend.resources.elements.elaw`
- `properties`
- `typing`

## Classe: `Seletores`

Gerencie seletores e ações para o fluxo de solicitação Elaw.

**Herda de:** `Geral`

### Métodos

#### `informa_tipo_condenacao()`

Informe o tipo de condenação no campo apropriado.

Esta função seleciona o tipo de condenação (Sentença, Acordão, etc)
no formulário do sistema Elaw, utilizando os dados do bot.

**Parâmetros:**

- `self` (Any)

#### `informa_tipo_custa()`

Informe o tipo de custa no campo correspondente.

Esta função seleciona o tipo de custa no formulário do Elaw.

**Parâmetros:**

- `self` (Any)

#### `conta_debito()`

Informe a conta de débito no campo correspondente.

Args:
    conta_debito (str): Conta de débito a ser informada.

**Parâmetros:**

- `self` (Any)
- `conta_debito` (str)

