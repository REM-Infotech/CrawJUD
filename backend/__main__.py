"""Entrada MAIN do backend."""

from __future__ import annotations

import logging

from backend import _start_backend

_defaultFormatter = logging.Formatter()  # noqa: N816

type AnyType = any


if __name__ == "__main__":
    _start_backend()

    while True:
        ...
