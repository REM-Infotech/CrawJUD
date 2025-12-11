from dataclasses import dataclass

from backend.api._forms.head import FormBot


@dataclass(match_args=False)
class OnlyFile(FormBot):
    """Represente um formulário para upload de arquivo único.

    Args:
        bot_id (str): Identificador do bot.
        sid_filesocket (str): ID da sessão do socket de arquivos.
        planilha_xlsx (str): Caminho da planilha Excel.

    """

    bot_id: str
    sid_filesocket: str
    xlsx: str
