"""Rotas de API/Socketio para bots."""

from ._api_routes import bots
from ._sio_routes import BotNS

__all__ = ["BotNS", "bots"]
