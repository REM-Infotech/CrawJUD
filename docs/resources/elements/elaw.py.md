# resources/elements/elaw.py

## Propósito

Update ElawAme module docstring to Google style.

This module provides selectors for automating ELAW operations.

## Dependências Principais

- `typing`

## Constantes

- `LINK_PROCESSO_LIST`

## Classe: `SolicitaPagamento`

Defina seletores e tipos para solicitações de pagamento ELAW.

### Atributos

- `TIPOS_PAGAMENTOS` (ClassVar[dict[str, str]])

## Classe: `PgtoCondenacao`

Defina seletores para pagamentos de condenação no ELAW.

**Herda de:** `SolicitaPagamento`

## Classe: `PgtoCustas`

Defina seletores para pagamentos de custas no ELAW.

**Herda de:** `SolicitaPagamento`

## Classe: `AtualizaFase`

Defina seletores para atualizar fases no ELAW.

