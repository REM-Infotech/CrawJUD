"""Módulo de agrupamento de Iterators para o CrawJUD."""

from __future__ import annotations

from typing import TYPE_CHECKING, TypedDict

from backend.common.exceptions.validacao import (
    ValidacaoStringError,
)
from backend.types_app.bot import ProcessoCNJ

if TYPE_CHECKING:
    from backend.interfaces import BotData
    from backend.task_manager.controllers.pje import PJeBot


class DictSeparaRegiao(TypedDict):
    """Define o dicionário que separa regiões e posições de processos.

    Args:
        regioes (dict[str, list[BotData]]): Dicionário de regiões e bots.
        position_process (dict[str, int]): Posição dos processos por região.

    """

    regioes: dict[str, list[BotData]]
    position_process: dict[ProcessoCNJ, int]


class RegioesIterator[T: BotData]:
    """Retorne regiões e dados associados iterando sobre processos separados.

    Args:
        bot (PJeBot): Instância do bot para acessar métodos e dados.

    Returns:
        RegioesIterator: Iterador sobre tuplas (região, dados da região).

    Raises:
        StopIteration: Quando todas as regiões forem iteradas.

    """

    def __init__(self, bot: PJeBot) -> None:
        """Inicialize o iterador de regiões com dados do bot e processos separados.

        Args:
            bot (PJeBot): Instância do bot para acessar métodos e dados.


        """
        # Carrega arquivos e separa regiões
        self._bot = bot

        processos: DictSeparaRegiao = self.separar_regiao()

        self._regioes = list(processos["regioes"].items())
        self._posicoes_processos_planilha = processos["position_process"]
        self._index = 0

        # Atualiza atributos do bot
        bot.posicoes_processos = self._posicoes_processos_planilha
        bot.total_rows = len(self._posicoes_processos_planilha.values())

    def __iter__(self) -> RegioesIterator[list[T]]:
        """Retorne o próprio iterador para permitir iteração sobre regiões.

        Returns:
            RegioesIterator: O próprio iterador de regiões.

        """
        return self

    def __next__(self) -> T:
        """Implementa a iteração retornando próxima região e dados associados.

        Returns:
            tuple[str, str]: Tupla contendo a região e os dados da região.

        Raises:
            StopIteration: Quando todas as regiões forem iteradas.

        """
        if self._index >= len(self._regioes):
            raise StopIteration

        regiao, data_regiao = self._regioes[self._index]
        self._bot.regiao = regiao
        self._bot.data_regiao = data_regiao
        self._index += 1
        return data_regiao

    def separar_regiao(self) -> DictSeparaRegiao:
        """Separa os processos por região a partir do número do processo.

        Returns:
            dict[str, list[BotData] | dict[str, int]]: Dicionário com as regiões e a
            posição de cada processo.

        """
        regioes_dict: dict[str, list[BotData]] = {}
        position_process: dict[str, int] = {}

        for item in self._bot.frame:
            try:
                numero_processo = ProcessoCNJ(
                    item["NUMERO_PROCESSO"],
                )

                regiao = numero_processo.tj
                # Atualiza o número do processo no item
                item["NUMERO_PROCESSO"] = str(numero_processo)
                # Adiciona a posição do processo na
                # lista original no dicionário de posições
                position_process[numero_processo] = len(
                    position_process,
                )

                # Caso a região não exista no dicionário, cria uma nova lista
                if not regioes_dict.get(regiao):
                    regioes_dict[regiao] = [item]
                    continue

                # Caso a região já exista, adiciona o item à lista correspondente
                regioes_dict[regiao].append(item)

            except ValidacaoStringError:
                continue

        return {
            "regioes": regioes_dict,
            "position_process": position_process,
        }
