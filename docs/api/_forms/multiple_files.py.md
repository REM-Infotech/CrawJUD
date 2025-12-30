# api/_forms/multiple_files.py

## Propósito

Módulo do sistema CrawJUD.

## Dependências Principais

- `__future__`
- `backend.api._forms.head`
- `dataclasses`

## Classe: `MultipleFiles`

Represente um formulário para múltiplos arquivos anexados.

Args:
    bot_id (str): Identificador do bot.
    sid_filesocket (str): ID da sessão do socket de arquivos.
    credencial (str): Credencial de acesso.
    xlsx (str): Caminho da planilha Excel.
    anexos (list[str]): Lista de arquivos anexos.

**Herda de:** `FormBot`

### Atributos

- `bot_id` (str)
- `sid_filesocket` (str)
- `credencial` (str)
- `xlsx` (str)
- `anexos` (list[str])

