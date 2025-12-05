from queue import Queue
from time import sleep
from typing import NoReturn

from rich.console import Console
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.text import Text

queue = Queue()
main_console = Console()


def log(message: str, target: str) -> None:
    queue.put((target, message))


def run_console() -> NoReturn:
    layout = Layout(name="root")

    titles = {
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

    logs = {"backend.api": [], "backend.task_manager": []}

    live = Live(layout, console=main_console, refresh_per_second=5, screen=True)

    def remove_logs() -> None:
        if len(logs[target]) >= live.console.height - 2:
            remove = (len(logs[target]) - (live.console.height - 2)) - 1

            if remove < 0:
                remove = 0

            logs[target] = logs[target][remove:]

    def update_panel() -> None:
        layout[target].update(
            Panel(
                Text.from_ansi("\n".join(logs[target]), style="cyan"),
                title=titles[target]["text"],
                style=titles[target]["style"],
            ),
        )
        live.update(layout)

    with live:
        while True:
            target = None
            message = None
            while queue.empty():
                ...

            sleep(0.2)
            target, message = queue.get()
            message = str(message)

            if "\n" in message:
                message = message.splitlines()
                for msg in message:
                    remove_logs()
                    logs[target].append(msg)
                    update_panel()

                continue

            remove_logs()
            logs[target].append(message)
            update_panel()
