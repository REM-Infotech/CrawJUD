# interfaces/pje/__init__.py

## Propósito

Defina interfaces e tipos para integração com o PJe.

Este pacote contém definições de tipos e interfaces para
facilitar a integração com o sistema PJe.

## Dependências Principais

- `__future__`
- `backend.types_app`
- `typing`
- `worksheet`

## Classe: `DictResults`

Define os resultados retornados pelo desafio do PJe.

Args:
    id_processo (str): Identificador do processo.
    captchatoken (str): Token do captcha.
    text (str): Texto de resposta.
    data_request (Processo): Dados do processo retornados.

Returns:
    DictResults: Dicionário com informações dos resultados do desafio.

**Herda de:** `TypedDict`

### Atributos

- `id_processo` (str)
- `data_request` (Dict)

