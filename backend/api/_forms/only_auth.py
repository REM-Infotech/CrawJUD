from __future__ import annotations

from dataclasses import dataclass

from backend.api._forms.head import FormBot


@dataclass(match_args=False)
class OnlyAuth(FormBot):
    """Represente um formulário para autenticação sem upload de arquivo.

    Args:
        bot_id (str): Identificador do bot.
        sid_filesocket (str): ID da sessão do socket de arquivos.
        credencial (str): Credencial de acesso.

    """

    bot_id: str
    sid_filesocket: str
    credencial: str
