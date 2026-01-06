"""Gerencia fila e salvamento assíncrono de erros em arquivos Excel."""

from __future__ import annotations

from datetime import datetime
from queue import Queue
from threading import Thread
from typing import TYPE_CHECKING, NoReturn
from zoneinfo import ZoneInfo

from pandas import DataFrame

from backend.interfaces import DataSave
from backend.resources.iterators.queues import QueueIterator
from backend.resources.queues.file_operation.main import (
    FileOperator,
)

if TYPE_CHECKING:
    from backend.controllers.head import CrawJUD
    from typings import Dict

DATASAVE = []


class SaveError(FileOperator):
    """Controle da Queue de salvamento de erros."""

    def __init__(self, bot: CrawJUD) -> None:
        """Instancia da queue de salvamento de erros."""
        self.bot = bot
        self.queue_save = Queue()
        self.thead_save = Thread(target=self.save_error, daemon=True)
        self.thead_save.start()

    def __call__(
        self,
        worksheet: str = "Erros",
        data_save: list[Dict] | None = None,
    ) -> None:
        """Adiciona dados de erro à fila para salvamento assíncrono.

        Args:
            worksheet (str): Nome da planilha de destino.
            data_save (list[Dict]): Lista de dados de erro a serem salvos.

        """
        if data_save:
            self.queue_save.put_nowait({
                "worksheet": worksheet,
                "data_save": DataFrame(data_save).to_dict(
                    orient="records"
                ),
            })

    def save_error(self) -> NoReturn:
        """Salve erros da fila em arquivo Excel de forma assíncrona."""
        tz = ZoneInfo("America/Sao_Paulo")
        now = datetime.now(tz=tz).strftime("%d-%m-%Y %H-%M-%S")
        nome_arquivo = f"Erros - PID {self.bot.pid} - {now}.xlsx"
        arquivo_erro = self.bot.output_dir_path.joinpath(nome_arquivo)

        for data in QueueIterator[DataSave](self.queue_save):
            if data and len(data["data_save"]) > 0:
                self.save_file(data=data, arquivo_xlsx=arquivo_erro)
