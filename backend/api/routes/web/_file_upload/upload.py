"""Gerencie uploads de arquivos e envio ao storage via fila."""

from __future__ import annotations

import asyncio
from contextlib import suppress
from io import BytesIO
from pathlib import Path
from queue import Empty, Queue, ShutDown
from threading import Thread
from time import sleep
from typing import Self, TypedDict

from quart import request

from backend.api.resources import formata_string
from backend.extensions import app, storage

WORKDIR = Path.cwd()


class DataFileUpload(TypedDict):
    """Defina os campos necessários para upload de arquivo.

    name: Nome do arquivo.
    fileSize: Tamanho do arquivo em bytes.
    chunk: Dados do arquivo em bytes.
    """

    name: str
    fileSize: int
    chunk: bytes
    seed: str


class IterQueueFile:
    """Itere sobre itens de uma fila de uploads de arquivos.

    Permite consumir itens da fila um a um, útil para processar uploads.
    """

    def __init__(self, queue: Queue) -> None:
        """Inicialize com a fila de uploads de arquivos.

        Args:
            queue (Queue): Fila de uploads de arquivos.

        """
        self.queue = queue

    def __iter__(self) -> Self:
        """Retorne o próprio iterador para iteração.

        Returns:
            Self: O próprio iterador.

        """
        return self

    def __next__(self) -> DataFileUpload:
        """Retorne o próximo item da fila ou encerre a iteração.

        Returns:
            DataFileUpload: Próximo item da fila.

        Raises:
            StopIteration: Quando a fila é encerrada.

        """
        while self.queue.empty():
            ...

        try:
            return self.queue.get_nowait()

        except Empty:
            return None

        except ShutDown:
            raise StopIteration from None


class FileUploader:
    """Gerencie uploads de arquivos e envio ao storage.

    Métodos:
        upload_file: Faça upload de um arquivo em partes.
        queue_upload: Consuma a fila de uploads.
    """

    @property
    def sid(self) -> str:
        return self._sid

    @sid.setter
    def sid(self, val: str) -> None:
        self._sid = val

    @property
    def bucket_name(self) -> str:
        return app.config["MINIO_BUCKET_NAME"]

    def __init__(self) -> None:
        """Inicialize o FileUploader e crie a thread de upload."""
        self.queue_upload_file = Queue()
        self.thread_upload_file = Thread(target=self.queue_upload, daemon=True)
        self.thread_upload_file.start()

    def __call__(self, data: DataFileUpload) -> None:
        self.sid = request.sid
        self.queue_upload_file.put_nowait(data)

    def upload_file(self, data: DataFileUpload) -> None:

        seed = data["seed"]
        output = WORKDIR.joinpath("output", seed)
        filename = formata_string(data["name"])
        path_file = output.joinpath(filename)
        output.mkdir(exist_ok=True, parents=True)
        sleep(0.25)
        object_path = Path(seed).joinpath(filename).as_posix()

        mode = "ab"
        if not path_file.exists():
            mode = "wb"

        with path_file.open(mode=mode) as fp:
            fp.write(data["chunk"])

        with suppress(Exception):
            if path_file.stat().st_size >= data["fileSize"]:
                self.__upload_storage(
                    object_path=object_path,
                    path_file=path_file,
                )

    def __upload_storage(self, object_path: str, path_file: Path) -> None:

        sz = path_file.stat().st_size
        obj = object_path
        bucket = self.bucket_name
        storage.put_object(bucket, obj, data=BytesIO(path_file.read_bytes()), length=sz)

        path_file.unlink()
        path_file.parent.rmdir()

    def queue_upload(self) -> None:

        with asyncio.Runner() as runner:
            runner.run(self._queue_upload())

    async def _queue_upload(self) -> None:
        async with app.app_context():
            for data in IterQueueFile(self.queue_upload_file):
                if data:
                    self.upload_file(data=data)


uploader = FileUploader()
