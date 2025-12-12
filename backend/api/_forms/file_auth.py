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
    sid_filesocket: str
    credencial: str
    xlsx: str


@dataclass(match_args=False)
class Pje(FormBot):
    """Represente um formulário para protocolo PJe com certificado digital.

    Args:
        bot_id (str): Identificador do bot.
        sid_filesocket (str): ID da sessão do socket de arquivos.
        xlsx (str): Caminho da planilha Excel.
        certificado (str): Caminho do certificado digital.
        senha_certificado (str): Senha do certificado digital.

    """

    __name__ = "pje"

    bot_id: str
    sid_filesocket: str
    xlsx: str
    cpf_cnpj_certificado: str
    certificado: str
    senha_certificado: str
    kdbx: str
    senha_kdbx: str
