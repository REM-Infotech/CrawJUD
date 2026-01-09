"""Decoradores do app."""

from __future__ import annotations

from backend.api.decorators._api import CrossDomain, jwt_sio_required

__all__ = ["CrossDomain", "jwt_sio_required"]
