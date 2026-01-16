# ruff: noqa: D101, D107

"""Log bot."""

from __future__ import annotations

from asyncio import create_task
from typing import TypedDict, Unpack

from quart_socketio import Namespace, SocketIO

from backend.api.decorators import async_jwt_required

from .upload import uploader


class FileUploadArguments(TypedDict):
    name: str
    chunk: bytes
    current_size: int
    fileSize: int
    fileType: str
    seed: str


fileupload = set()


class FileUploadNamespace(Namespace):
    def __init__(self, socketio: SocketIO = None) -> None:
        namespace = "/files"
        super().__init__(namespace, socketio)

    @async_jwt_required
    def on_connect(self) -> None: ...

    @async_jwt_required
    async def on_add_file(self, **data: Unpack[FileUploadArguments]) -> None:
        """Log bot."""
        fileupload.add(create_task(uploader(data)).add_done_callback(fileupload.discard))
        print(data["name"])
