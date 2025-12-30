from __future__ import annotations

from traceback import format_exception
from typing import TYPE_CHECKING

from tqdm import tqdm

from backend.controllers.jusds import JusDsBot

if TYPE_CHECKING:
    from backend.controllers.head import BotIterator
    from backend.interfaces import BotData


class Provisionamento(JusDsBot):
    name = "jusds_provisionamento"

    bot_data: BotData

    def execution(self) -> None:

        list_item: BotIterator[BotData] = self.frame
        for pos, item in enumerate(list_item):
            self.bot_data = item
            self.row = pos

    def queue(self) -> None:

        try:
            if self.search():
                print("ok")  # noqa: T201

        except Exception as e:  # noqa: BLE001
            exc = format_exception(e)
            tqdm.write("\n".join(exc))
