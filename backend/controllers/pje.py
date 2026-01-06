"""Módulo para a classe de controle dos robôs PJe."""

from __future__ import annotations

from abc import abstractmethod
from concurrent.futures import ThreadPoolExecutor
from contextlib import suppress
from time import sleep
from typing import TYPE_CHECKING, ClassVar

from dotenv import load_dotenv
from httpx import Client

from backend.controllers.head import CrawJUD
from backend.resources import RegioesIterator
from backend.resources.auth.pje import AutenticadorPJe
from backend.resources.search.pje import PjeSeach

if TYPE_CHECKING:
    from backend.dicionarios import BotData
    from backend.resources.queues.file_downloader import (
        FileDownloader,
    )
    from typings import Dict, ProcessoCNJ

load_dotenv()


class PJeBot(CrawJUD):
    """Classe de controle para robôs do PJe."""

    _regiao: ClassVar[int] = 1
    _is_grau_list: ClassVar[bool] = False
    download_file: FileDownloader
    posicoes_processos: ClassVar[dict[str, str]] = {}

    auth: AutenticadorPJe

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

    def execution(self) -> None:

        generator_regioes = RegioesIterator(bot=self)
        self.total_rows = len(self.posicoes_processos)

        for data_regiao in generator_regioes:
            if self.bot_stopped.is_set():
                break

            with suppress(Exception):
                if self.auth():
                    self.queue_regiao(data=data_regiao)

        self.finalizar_execucao()

    def queue_regiao(self, data: list[BotData]) -> None:
        """Enfileire processos judiciais para processamento.

        Args:
            data (list[BotData]): Lista de dados dos processos.

        """
        url = f"https://pje.trt{self.regiao}.jus.br/pjekz"
        cookies = self.auth.get_cookies()
        headers = self.auth.get_headers(url=url)

        client_context = Client(cookies=cookies, headers=headers)
        thread_pool = ThreadPoolExecutor(6)

        with client_context as client, thread_pool as pool:
            for item in data:
                if self.bot_stopped.is_set():
                    break

                pool.submit(self.queue, item=item, client=client)
                sleep(5)

    @abstractmethod
    def queue(self, item: BotData, client: Client): ...  # noqa: ANN201
