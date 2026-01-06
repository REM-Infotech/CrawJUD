"""Tipos de resposta para a aplicação types_app.responses."""

from __future__ import annotations

from typing import TypedDict


class PayloadDownloadExecucao(TypedDict):
    content: str
    file_name: str
