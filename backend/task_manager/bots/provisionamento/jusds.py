from __future__ import annotations

from typing import TYPE_CHECKING

from backend.task_manager.controllers.jusds import JusDsBot

if TYPE_CHECKING:
    from backend.interfaces import BotData
    from backend.task_manager.controllers.head import BotIterator


class Provisionamento(JusDsBot):
    name = "jusds_provisionamento"

    def execution(self) -> None:

        list_item: BotIterator[BotData] = self.frame
        for item in list_item:
            print(item)  # noqa: T201
