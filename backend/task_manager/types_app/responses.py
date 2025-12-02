"""Módulo de respostas do aplicativo."""

from __future__ import annotations

from typing import TypedDict

from flask import Response


class PayloadDownloadExecucao(TypedDict):
    """Defina o payload para download de execução de arquivos.

    Args:
        file_name (str): Nome do arquivo.
        content (str): Conteúdo do arquivo.

    """

    file_name: str
    content: str


class Response[T](Response):
    """Classe de resposta genérica para APIs."""
