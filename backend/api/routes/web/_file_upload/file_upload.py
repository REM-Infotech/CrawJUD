"""Log bot."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flask_jwt_extended import jwt_required
from quart_socketio import Namespace, SocketIO

from .upload import uploader

if TYPE_CHECKING:
    from typings import Any


class FileUploadNamespace(Namespace):
    def __init__(self, socketio: SocketIO = None) -> None:
        namespace = "/files"
        super().__init__(namespace, socketio)

    @jwt_required()
    def on_add_file(self, data: dict[str, Any]) -> None:
        """Log bot."""
        uploader(data)
