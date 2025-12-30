"""Gerencie downloads de arquivos em fila com suporte a múltiplas threads.

Este módulo fornece:
- FileDownload: dicionário tipado para tarefas de download de arquivos.
- FileDownloader: classe para gerenciar e executar downloads em fila,
  utilizando uma thread dedicada e suporte a cookies HTTP.
"""

from __future__ import annotations

from pathlib import Path
from queue import Queue
from threading import Thread
from time import sleep
from traceback import format_exception
from typing import TypedDict

from httpx import Client
from tqdm import tqdm

from backend.resources.iterators.queues import QueueIterator

BUFFER_1MB = 1024 * 1024
CHUNK_8MB = 8192 * 1024


class FileDownload(TypedDict):
    """Defina o dicionário para informações de download de arquivo.

    Args:
        link_file (str): URL do arquivo para download.
        file (str): Caminho do arquivo de destino.
        cookies (dict[str, str]): Cookies HTTP para autenticação.

    """

    link_file: str
    file: str
    cookies: dict[str, str]


class FileDownloader:
    """Gerencie downloads de arquivos em uma fila usando thread dedicada.

    Permite adicionar tarefas de download em uma fila e processa cada
    tarefa em uma thread separada, realizando o download dos arquivos
    especificados.
    """

    def __init__(self) -> None:
        """Inicialize o gerenciador de downloads e inicie a thread da fila."""
        self.queue = Queue()
        self.thread = Thread(
            target=self.queue_download,
            daemon=True,
            name="Download de Arquivos",
        )
        self.thread.start()

    def queue_download(self) -> None:
        """Consuma a fila de downloads e realize o download dos arquivos."""
        client = Client()

        for file_download in QueueIterator[FileDownload](self.queue):
            if not file_download:
                continue

            try:
                stream_kw = {
                    "method": "GET",
                    "url": file_download["link_file"],
                    "cookies": file_download["cookies"],
                }

                file_path = Path(file_download["file"])
                file_path.parent.mkdir(
                    parents=True,
                    exist_ok=True,
                )  # BUGFIX: garante que o diretório existe

                with (
                    client.stream(**stream_kw) as stream,
                    file_path.open("wb", buffering=BUFFER_1MB) as fp,
                ):
                    for chunk in stream.iter_bytes(chunk_size=CHUNK_8MB):
                        fp.write(chunk)

            except Exception as e:
                tqdm.write("\n".join(format_exception(e)))

            sleep(1)

    def __call__(self, file: str, link: str, cookies: dict[str, str]) -> None:
        """Adicione uma nova tarefa de download à fila.

        Args:
            file (str): Caminho do arquivo de destino.
            link (str): URL do arquivo para download.
            cookies (dict[str, str]): Cookies HTTP para autenticação.

        """
        self.queue.put_nowait(
            FileDownload(
                link_file=link,
                file=file,
                cookies=cookies,
            ),
        )
