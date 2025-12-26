"""Entrada MAIN do backend."""

from __future__ import annotations

import logging
import sys

from backend import _start_backend, app

_defaultFormatter = logging.Formatter()  # noqa: N816

type AnyType = any


if __name__ == "__main__" and "debugpy" in sys.modules:
    _start_backend()

    while True:
        ...
elif __name__ == "__main__":
    app()
