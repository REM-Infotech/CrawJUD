# api/_forms/only_file.py

## Propósito

Módulo do sistema CrawJUD.

## Dependências Principais

- `backend.api._forms.head`
- `dataclasses`

## Classe: `OnlyFile`

Represente um formulário para upload de arquivo único.

Args:
    bot_id (str): Identificador do bot.
    sid_filesocket (str): ID da sessão do socket de arquivos.
    xlsx (str): Caminho da planilha Excel.

**Herda de:** `FormBot`

### Atributos

- `bot_id` (str)
- `sid_filesocket` (str)
- `xlsx` (str)

