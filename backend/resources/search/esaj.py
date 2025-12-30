"""Implemente funcionalidades de busca para o sistema ESAJ.

Este módulo contém a classe SearhEsaj, responsável por executar
operações de busca utilizando o bot específico do ESAJ.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from backend.resources.search.main import SearchBot

if TYPE_CHECKING:
    from backend.types_app import AnyType


class SearhEsaj(SearchBot):
    """Implemente o sistema de busca para o sistema ESAJ."""

    def __call__(self, *args: AnyType, **kwargs: AnyType) -> None:
        """Execute a chamada do bot de busca ESAJ.

        Args:
            *args (AnyType): Argumentos posicionais.
            **kwargs (AnyType): Argumentos nomeados.

        """
