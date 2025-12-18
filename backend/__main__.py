"""Entrada MAIN do backend."""

from __future__ import annotations

import logging

from backend import _start_backend

_defaultFormatter = logging.Formatter()  # noqa: N816

type AnyType = any


class CustomStreamHandler(logging.StreamHandler):  # noqa: D101
    def format(self, record: logging.LogRecord) -> str:
        return _defaultFormatter.format(record)

    def emit(self, record: logging.LogRecord) -> None:
        msg = self.format(record)
        print(name_record=record.name, *(msg,))  # noqa: B026, T201


if __name__ == "__main__":
    _start_backend()

    while True:
        ...
