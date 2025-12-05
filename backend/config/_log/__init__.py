from __future__ import annotations

import builtins
import inspect
from contextlib import contextmanager
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Generator


class CustomLog:
    @contextmanager
    @staticmethod
    def _custom_print() -> Generator[None]:
        original_print = builtins.print

        def rich_print(*args, **kwargs) -> None:
            frame = inspect.currentframe()
            modulo = inspect.getmodule(frame.f_back)
            message = " ".join(str(arg) for arg in args)
            target = "backend.api"
            if "celery" in modulo.__name__ or "kombu" in modulo.__name__:
                target = "backend.task_manager"

            from backend.config._log._layout_console import log

            log(message, target)

        builtins.print = rich_print
        yield
        builtins.print = original_print
