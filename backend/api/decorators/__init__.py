"""Decoradores do app."""

from __future__ import annotations

from functools import wraps
from typing import TYPE_CHECKING

from flask_jwt_extended import verify_jwt_in_request

from backend.api.decorators._api import CrossDomain

if TYPE_CHECKING:
    from collections.abc import Callable

__all__ = ["CrossDomain"]


def jwt_sio_required[**P, T](fn: Callable[P, T]) -> Callable[P, T]:

    @wraps(fn)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> Callable[P, T]:

        verify_jwt_in_request()
        return fn(*args, **kwargs)

    return wrapper
