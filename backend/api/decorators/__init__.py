"""Decoradores do app."""

from __future__ import annotations

from backend.api.decorators._api import CrossDomain, async_jwt_required

__all__ = ["CrossDomain", "async_jwt_required"]
