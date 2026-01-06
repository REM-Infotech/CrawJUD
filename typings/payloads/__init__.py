"""Tipos de resposta para a aplicação types_app.responses."""

from typing import TypedDict


class PayloadDownloadExecucao(TypedDict):
    content: str
    file_name: str
