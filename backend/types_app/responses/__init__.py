"""Tipos de resposta para a aplicação types_app.responses."""

from typing import TypedDict


class PayloadDownloadExecucao(TypedDict):
    """Dicionário tipado para payload de download de execução.

    Attributes
    ----------
    content : str
        Conteúdo do arquivo a ser baixado.
    file_name : str
        Nome do arquivo a ser baixado.

    """

    content: str
    file_name: str
