"""Defina interfaces e tipos para integração com o PJe.

Este pacote contém definições de tipos e interfaces para
facilitar a integração com o sistema PJe.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypedDict

from .worksheet import CapaPJe

if TYPE_CHECKING:
    from backend.types_app import Dict


class DictResults(TypedDict):
    """Define os resultados retornados pelo desafio do PJe.

    Args:
        id_processo (str): Identificador do processo.
        captchatoken (str): Token do captcha.
        text (str): Texto de resposta.
        data_request (Processo): Dados do processo retornados.

    Returns:
        DictResults: Dicionário com informações dos resultados do desafio.

    """

    id_processo: str
    data_request: Dict


__all__ = [
    "CapaPJe",
]
