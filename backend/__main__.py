"""Entrada MAIN do backend."""

from __future__ import annotations

from typing import TYPE_CHECKING, Literal

from backend import _start_backend

if TYPE_CHECKING:
    from threading import Thread

if __name__ == "__main__":
    _threads: dict[Literal["threads"], list[Thread]] = _start_backend()
    while True:
        ...
