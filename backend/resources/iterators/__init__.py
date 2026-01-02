"""Iterator para os dados inputados na planilha."""

from __future__ import annotations

from io import BytesIO
from typing import TYPE_CHECKING, Self

from pandas import read_excel

from backend.interfaces import BotData
from backend.resources.formatadores import (
    format_data,
    format_float,
    formata_string,
)

if TYPE_CHECKING:
    from backend.controllers.head import CrawJUD


class BotIterator[T: BotData]:
    """Iterator para os dados inputados na planilha."""

    def __init__(self, bot: CrawJUD) -> None:
        """Instancia o iterator para os dados inputados na planilha."""
        self._index = 0

        path_xlsx = bot.output_dir_path.joinpath(
            formata_string(bot.xlsx),
        )

        if path_xlsx.exists():
            df = read_excel(BytesIO(path_xlsx.read_bytes()), engine="openpyxl")
            df.columns = df.columns.str.upper()

            for col in df.columns:
                df[col] = df[col].apply(format_data)

            for col in df.select_dtypes(include=["float"]).columns:
                df[col] = df[col].apply(format_float)

            data_bot: list[BotData] = []
            to_dict = df.to_dict(orient="records")
            unformatted = [BotData(list(item.items())) for item in to_dict]

            for item in unformatted:
                dt = {}

                for k, v in list(item.items()):
                    dt[k.upper()] = v

                if dt:
                    data_bot.append(dt)

            self._frame = data_bot
            bot.total_rows = len(self._frame)

    def __iter__(self) -> Self[T]:
        """Retorne o próprio iterador para permitir iteração sobre regiões.

        Returns:
            RegioesIterator: O próprio iterador de regiões.

        """
        return self

    def __next__(self) -> T:
        """Implementa a iteração retornando próxima região e dados associados.

        Returns:
            tuple[str, str]: Tupla contendo a região e os dados da região.

        Raises:
            StopIteration: Quando todas as regiões forem iteradas.

        """
        if self._index >= len(self._frame):
            raise StopIteration

        data = self._frame[self._index]
        self._index += 1
        return data
