# ruff: noqa: T201, BLE001
from __future__ import annotations

from traceback import format_exception
from typing import TYPE_CHECKING

from tqdm import tqdm

from backend.controllers.jusds import JusDsBot

if TYPE_CHECKING:
    from backend.controllers.head import BotIterator
    from backend.dicionarios import JusdsProvisionamento


class Provisionamento(JusDsBot):
    name = "jusds_provisionamento"

    def execution(self) -> None:

        list_item: BotIterator[JusdsProvisionamento] = self.frame
        for pos, item in enumerate(list_item):
            self.bot_data = item
            self.row = pos

    def queue(self) -> None:

        try:
            if self.search():
                print("ok")

        except Exception as e:
            exc = format_exception(e)
            tqdm.write("\n".join(exc))
