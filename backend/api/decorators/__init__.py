"""Decoradores do app."""

from __future__ import annotations

from contextlib import suppress
from functools import wraps
from typing import TYPE_CHECKING, ParamSpec

from flask import current_app
from flask_jwt_extended import verify_jwt_in_request

from backend.api.decorators._api import CrossDomain

if TYPE_CHECKING:
    from collections.abc import Callable

__all__ = ["CrossDomain"]

type AnyType = any

P = ParamSpec("P")


def jwt_sio_required[T](fn: Callable[P, T]) -> Callable[P, T]:

    @wraps(fn)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> Callable[P, T]:

        with suppress(Exception):
            verify_jwt_in_request()
            return fn(*args, **kwargs)

        return None

    return wrapper
