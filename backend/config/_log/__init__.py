from __future__ import annotations

import inspect
import sys
from contextlib import contextmanager
from typing import TYPE_CHECKING, ClassVar

from rich.console import Console
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.text import Text

if TYPE_CHECKING:
    from collections.abc import Generator


type AnyType = any
main_console = Console()


class CustomLog:
    layout = Layout(name="root")
    titles: ClassVar[dict] = {
        "backend.api": {
            "text": "Backend API",
            "style": "bold green",
        },
        "backend.task_manager": {
            "text": "Backend Task Manager",
            "style": "bold magenta",
        },
    }
    layout.split_row(
        Layout(Panel(""), name="backend.api"),
        Layout(Panel(""), name="backend.task_manager"),
    )

    logs: ClassVar[dict] = {"backend.api": [], "backend.task_manager": []}
    live = Live(
        layout,
        console=main_console,
        refresh_per_second=5,
        screen=("debugpy" not in sys.modules),
    )

    @contextmanager
    @staticmethod
    def print_replacer() -> Generator[None]:

        import builtins

        original_print = builtins.print

        def rich_print(
            *args: AnyType,
            **kwargs: AnyType,
        ) -> None:

            name_record = kwargs.get("name_record")
            frame = inspect.currentframe()
            modulo = inspect.getmodule(frame.f_back)
            message = " ".join(str(arg) for arg in args)
            original_print(message)
            return
            target = "backend.api"

            if any([
                "celery" in modulo.__name__,
                "kombu" in modulo.__name__,
                name_record and "celery" in name_record,
                name_record and "kombu" in name_record,
            ]):
                target = "backend.task_manager"

            if "\n" in message:
                message = message.splitlines()
                for msg in message:
                    CustomLog.remove_logs(target=target)
                    CustomLog.logs[target].append(msg)
                    CustomLog.update_panel(target=target)

                return

            CustomLog.remove_logs(target=target)
            CustomLog.logs[target].append(message)
            CustomLog.update_panel(target=target)

        builtins.print = rich_print
        yield
        builtins.print = original_print

    @staticmethod
    def remove_logs(target: str) -> None:
        if len(CustomLog.logs[target]) >= CustomLog.live.console.height - 2:
            remove = (
                len(CustomLog.logs[target]) - (CustomLog.live.console.height - 2)
            ) - 1

            if remove < 0:
                remove = 0

            CustomLog.logs[target] = CustomLog.logs[target][remove:]

    @staticmethod
    def update_panel(target: str) -> None:
        CustomLog.layout[target].update(
            Panel(
                Text.from_ansi("\n".join(CustomLog.logs[target]), style="cyan"),
                title=CustomLog.titles[target]["text"],
                style=CustomLog.titles[target]["style"],
            ),
        )
        CustomLog.live.update(CustomLog.layout)


@contextmanager
def print_replacer() -> Generator[None, AnyType]:
    """Context manager to replace print function temporarily."""
    import builtins

    original_print = builtins.print

    def custom_print(*args: AnyType, **kwargs: AnyType) -> None:
        original_print(*args, **kwargs)

    builtins.print = custom_print
    try:
        yield
    finally:
        builtins.print = original_print
