# task_manager/bots/admin/elaw/solicita_pagamento/inicializacao.py

## Propósito

Gerencie inicialização e seleção de pagamentos no Elaw.

Este módulo contém classes e funções para iniciar e selecionar
tipos de pagamento na interface do Elaw.

## Dependências Principais

- `__future__`
- `backend.common.raises`
- `backend.resources.driver`
- `backend.resources.elements.elaw`
- `properties`
- `selenium.common`
- `selenium.webdriver.support`
- `time`
- `traceback`
- `typing`

## Classe: `Inicializacao`

Inicialize e gerencie o fluxo de solicitação de pagamento.

Esta classe controla o acesso, criação e seleção de tipos de
pagamento na interface do Elaw.

**Herda de:** `Geral`

### Métodos

#### `novo_pagamento()`

Clique no botão para iniciar novo pagamento no Elaw.

Esta função aguarda o botão de novo pagamento estar disponível
e realiza o clique para iniciar o processo.

**Parâmetros:**

- `self` (Inicializacao)

#### `seleciona_tipo_pgto()`

Seleciona o tipo de pagamento no formulário do Elaw.

Returns:
    ISolicitacaoPagamentos: Solicitador do tipo de pagamento.

**Parâmetros:**

- `self` (Inicializacao)

**Retorna:** ISolicitacaoPagamentos

