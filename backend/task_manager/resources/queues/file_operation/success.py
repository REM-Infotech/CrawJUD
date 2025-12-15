"""Operações de planilhas."""

from __future__ import annotations

from datetime import datetime
from queue import Queue
from threading import Thread
from typing import TYPE_CHECKING, NoReturn
from zoneinfo import ZoneInfo

from pandas import DataFrame

from backend.interfaces import DataSave
from backend.task_manager.resources.iterators.queues import QueueIterator
from backend.task_manager.resources.queues.file_operation.main import (
    FileOperator,
)

if TYPE_CHECKING:
    from backend.task_manager.controllers.head import CrawJUD
DATASAVE = []


class SaveSuccess(FileOperator):
    """Controle da Queue de salvamento de sucessos."""

    bot: CrawJUD

    def __init__(self, bot: CrawJUD) -> None:
        """Instancia da queue de salvamento de erros."""
        self.bot = bot

        self.queue_save = Queue()
        self.thead_save = Thread(target=self.save_success, daemon=True)
        self.thead_save.start()

    def __call__(self, worksheet: str, data_save: str) -> None:
        """Adicione dados de sucesso à fila para processamento assíncrono.

        Args:
            worksheet (str): Nome da planilha de destino.
            data_save (str): Dados a serem salvos na planilha.

        """
        self.queue_save.put_nowait({
            "worksheet": worksheet,
            "data_save": DataFrame(data_save).to_dict(orient="records"),
        })

    def save_success(self) -> NoReturn:
        """Salve dados de sucesso em arquivo Excel de forma assíncrona."""
        tz = ZoneInfo("America/Sao_Paulo")
        now = datetime.now(tz=tz).strftime("%d-%m-%Y %H-%M-%S")
        nome_arquivo = f"Sucessos - PID {self.bot.pid} - {now}.xlsx"
        out_dir = self.bot.output_dir_path
        arquivo_sucesso = out_dir.joinpath(nome_arquivo)

        for data in QueueIterator[DataSave](self.queue_save):
            if data and len(data["data_save"]) > 0:
                self.save_file(data, arquivo_sucesso)
