from __future__ import annotations

from dataclasses import dataclass

from backend.api._forms.head import FormBot


@dataclass(match_args=False)
class MultipleFiles(FormBot):
    """Represente um formulário para múltiplos arquivos anexados.

    Args:
        bot_id (str): Identificador do bot.
        sid_filesocket (str): ID da sessão do socket de arquivos.
        credencial (str): Credencial de acesso.
        xlsx (str): Caminho da planilha Excel.
        anexos (list[str]): Lista de arquivos anexos.

    """

    bot_id: str
    sid_filesocket: str
    credencial: str
    xlsx: str
    anexos: list[str]
