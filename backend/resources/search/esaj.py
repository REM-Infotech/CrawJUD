"""Implemente funcionalidades de busca para o sistema ESAJ.

Este módulo contém a classe SearhEsaj, responsável por executar
operações de busca utilizando o bot específico do ESAJ.
"""

from __future__ import annotations

from backend.resources.search.main import SearchBot


class SearhEsaj(SearchBot):
    """Implemente o sistema de busca para o sistema ESAJ."""

    def __call__(self, *args: Any, **kwargs: Any) -> None:
        """Execute a chamada do bot de busca ESAJ.

        Args:
            *args (Any): Argumentos posicionais.
            **kwargs (Any): Argumentos nomeados.

        """
