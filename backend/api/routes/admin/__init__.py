"""Rotas de API/Socketio para gerenciamento de credenciais dos robôs."""

from ._api_routes import admin
from ._sio_routes import NamespaceAdminCrawJUD

__all__ = ["NamespaceAdminCrawJUD", "admin"]
