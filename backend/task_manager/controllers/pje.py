"""Módulo para a classe de controle dos robôs PJe."""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from dotenv import load_dotenv

from backend.task_manager.controllers.head import CrawJUD
from backend.task_manager.resources import RegioesIterator
from backend.task_manager.resources.auth.pje import AutenticadorPJe
from backend.task_manager.resources.search.pje import PjeSeach

if TYPE_CHECKING:
    from backend.task_manager.interfaces import BotData
    from backend.task_manager.resources.queues.file_downloader import (
        FileDownloader,
    )
    from backend.types_app import Dict
    from backend.types_app.bot import ProcessoCNJ

load_dotenv()


class PJeBot(CrawJUD):
    """Classe de controle para robôs do PJe."""

    download_file: FileDownloader
    posicoes_processos: ClassVar[Dict] = {}

    def __init__(self) -> None:
        """Inicialize o robô PJe com autenticação e busca."""
        self.auth = AutenticadorPJe(self)
        self.search = PjeSeach(self)

    # Retorna as posições dos processos por identificador.
    @property
    def list_posicao_processo(self) -> Dict[ProcessoCNJ, int]:
        """Liste as posições dos processos cadastrados.

        Returns:
            Dict[str, int]: Dicionário com posições dos processos.

        """
        return self.posicoes_processos

    @property
    def data_regiao(self) -> list[BotData]:
        """Obtenha a lista de dados das regiões cadastradas.

        Returns:
            list[BotData]: Lista de dados das regiões.

        """
        return self._data_regiao

    @data_regiao.setter
    def data_regiao(self, _data_regiao: list[BotData]) -> None:
        """Defina a lista de dados das regiões cadastradas.

        Args:
            _data_regiao (list[BotData]): Lista de dados das regiões.

        """
        self._data_regiao = _data_regiao

    @property
    def regiao(self) -> str:
        """Obtenha a região cadastrada.

        Returns:
            str: Região cadastrada.

        """
        # Retorna o valor da região atual
        return self._regiao

    @regiao.setter
    def regiao(self, _regiao: str) -> None:
        """Defina a região cadastrada.

        Args:
            _regiao (str): Região a ser definida.

        """
        # Define o valor da região
        self._regiao = _regiao

    def regioes(self) -> RegioesIterator:
        """Lista as regiões disponíveis do PJe.

        Returns:
            RegioesIterator: Iterador das regiões do PJe.

        """
        # Retorna um iterador das regiões
        return RegioesIterator(self)
