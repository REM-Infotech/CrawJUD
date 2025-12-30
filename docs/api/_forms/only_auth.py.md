# api/_forms/only_auth.py

## Propósito

Módulo do sistema CrawJUD.

## Dependências Principais

- `__future__`
- `backend.api._forms.head`
- `dataclasses`

## Classe: `OnlyAuth`

Represente um formulário para autenticação sem upload de arquivo.

Args:
    bot_id (str): Identificador do bot.
    sid_filesocket (str): ID da sessão do socket de arquivos.
    credencial (str): Credencial de acesso.

**Herda de:** `FormBot`

### Atributos

- `bot_id` (str)
- `sid_filesocket` (str)
- `credencial` (str)

