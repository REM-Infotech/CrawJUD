from __future__ import annotations

import asyncio
from traceback import format_exception
from typing import TYPE_CHECKING

from typer import Typer

if TYPE_CHECKING:
    from concurrent.futures import Future


typerapp = Typer()

futures: set[Future[None]] = set()


@typerapp.command(name="run")
def _thread_asgi() -> None:

    with asyncio.Runner() as runner:
        from app.extensions import create_app, sio

        try:
            app = runner.run(create_app())
            sio.run(app=app, port=5000)

        except Exception as e:  # noqa: BLE001
            exc = format_exception(e)
            print(exc)  # noqa: T201


__all__ = ["typerapp"]
