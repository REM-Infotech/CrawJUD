"""Implemente iteradores para manipular dados do ElawBot.

Este módulo fornece classes para iterar sobre dados de entrada
da planilha utilizados pelo ElawBot.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Self

from backend.dicionarios import ElawData

if TYPE_CHECKING:
    from backend.controllers.elaw import ElawBot
    from backend.dicionarios import BotData


class ElawIterator:
    """Implemente iteração sobre dados do ElawBot."""

    def __init__(self, bot: ElawBot) -> None:
        """Inicialize o iterador com a instância do ElawBot.

        Args:
            bot (ElawBot): Instância do ElawBot para iteração.

        """
        self._index = 0
        self.bot = bot
        self._frame = list(self.bot.frame)

    def __iter__(self) -> Self:
        """Retorne o próprio iterador.

        Returns:
            Self: O próprio objeto iterador.

        """
        return self

    def __next__(self) -> BotData:
        """Retorne o próximo item do iterador.

        Returns:
            BotData: Próximo item da iteração.

        Raises:
            StopIteration: Quando não houver mais itens.

        """
        if self._index >= len(self._frame):
            raise StopIteration

        data = self._frame[self._index]
        self._index += 1
        return ElawData(data)
