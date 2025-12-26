"""Entrada MAIN do backend."""

from __future__ import annotations

import logging

from backend import app

_defaultFormatter = logging.Formatter()  # noqa: N816

type AnyType = any


if __name__ == "__main__":
    app()
