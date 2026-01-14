"""Rotas Websocket."""

from .admin import AdminNamespace
from .bot import BotNamespace
from .file_upload import FileUploadNamespace

__all__ = ["AdminNamespace", "BotNamespace", "FileUploadNamespace"]
