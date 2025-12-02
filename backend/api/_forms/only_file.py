from dataclasses import dataclass

from api._forms.head import FormBot


@dataclass
class OnlyFile(FormBot):
    """Represente um formulário para upload de arquivo único.

    Args:
        bot_id (str): Identificador do bot.
        sid_filesocket (str): ID da sessão do socket de arquivos.
        planilha_xlsx (str): Caminho da planilha Excel.

    """

    bot_id: str
    sid_filesocket: str
    planilha_xlsx: str
