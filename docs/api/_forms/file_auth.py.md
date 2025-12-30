# api/_forms/file_auth.py

## Propósito

Módulo do sistema CrawJUD.

## Dependências Principais

- `backend.api._forms.head`
- `dataclasses`

## Classe: `FileAuth`

Represente um formulário para autenticação de arquivo.

Args:
    bot_id (str): Identificador do bot.
    sid_filesocket (str): ID da sessão do socket de arquivos.
    credencial (str): Credencial de acesso.
    xlsx (str): Caminho da planilha Excel.

**Herda de:** `FormBot`

### Atributos

- `bot_id` (str)
- `sid_filesocket` (str)
- `credencial` (str)
- `xlsx` (str)

