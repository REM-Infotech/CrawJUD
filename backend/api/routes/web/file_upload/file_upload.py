# ruff: noqa: D101, D107

"""Log bot."""

from __future__ import annotations

from typing import TYPE_CHECKING

from quart_socketio import Namespace, SocketIO

from backend.api.decorators import async_jwt_required

from .upload import uploader

if TYPE_CHECKING:
    from typings import Any


class FileUploadNamespace(Namespace):
    def __init__(self, socketio: SocketIO = None) -> None:
        namespace = "/files"
        super().__init__(namespace, socketio)

    @async_jwt_required
    def on_connect(self) -> None: ...

    @async_jwt_required
    def on_add_file(self, data: dict[str, Any]) -> None:
        """Log bot."""
        uploader(data)
