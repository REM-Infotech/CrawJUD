"""Rotas de API/Socketio para bots."""

from . import _sio_routes
from ._api_routes import bots

__all__ = ["_sio_routes", "bots"]
