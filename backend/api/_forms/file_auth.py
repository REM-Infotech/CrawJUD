from dataclasses import dataclass

from backend.api._forms.head import FormBot


@dataclass(match_args=False)
class FileAuth(FormBot):
    """Represente um formulário para autenticação de arquivo.

    Args:
        bot_id (str): Identificador do bot.
        sid_filesocket (str): ID da sessão do socket de arquivos.
        credencial (str): Credencial de acesso.
        xlsx (str): Caminho da planilha Excel.

    """

    bot_id: str
    credencial: str
    xlsx: str
