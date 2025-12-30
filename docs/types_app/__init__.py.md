# types_app/__init__.py

## Propósito

Defina tipos e aliases para uso em todo o projeto.

Este módulo centraliza definições de tipos e aliases
para padronizar e facilitar o desenvolvimento.

## Dependências Principais

- `__future__`
- `backend.types_app.bot`
- `backend.types_app.bot.string_types`
- `datetime`
- `os`
- `typing`

## Constantes

- `P`
- `T`

## Classe: `HealtCheck`

Defina informações de status do sistema para verificação.

Args:
    status (str): Situação geral do sistema.
    database (str): Situação do banco de dados.
    timestamp (str): Data e hora da verificação.

**Herda de:** `TypedDict`

### Atributos

- `status` (str)
- `database` (str)
- `timestamp` (str)

## Classe: `LoginForm`

Defina dados de login do usuário para autenticação.

Args:
    login (str): Nome de usuário.
    password (str): Senha do usuário.
    remember (bool): Se deve manter sessão ativa.

**Herda de:** `TypedDict`

### Atributos

- `login` (str)
- `password` (str)
- `remember` (bool)

