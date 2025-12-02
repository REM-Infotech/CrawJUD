from dataclasses import dataclass

from api._forms.head import FormBot


@dataclass
class FileAuth(FormBot):
    """Represente um formulário para autenticação de arquivo.

    Args:
        bot_id (str): Identificador do bot.
        sid_filesocket (str): ID da sessão do socket de arquivos.
        credencial (str): Credencial de acesso.
        planilha_xlsx (str): Caminho da planilha Excel.

    """

    bot_id: str
    sid_filesocket: str
    credencial: str
    planilha_xlsx: str


@dataclass
class Pje(FormBot):
    """Represente um formulário para protocolo PJe com certificado digital.

    Args:
        bot_id (str): Identificador do bot.
        sid_filesocket (str): ID da sessão do socket de arquivos.
        planilha_xlsx (str): Caminho da planilha Excel.
        certificado (str): Caminho do certificado digital.
        senha_certificado (str): Senha do certificado digital.

    """

    __name__ = "pje"

    bot_id: str
    sid_filesocket: str
    planilha_xlsx: str
