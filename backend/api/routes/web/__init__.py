"""Rotas Websocket."""

from ._admin import AdminNamespace
from ._bot import BotNamespace
from ._file_upload import FileUploadNamespace

__all__ = ["AdminNamespace", "BotNamespace", "FileUploadNamespace"]
