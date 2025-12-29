"""Gerencie operações de leitura e escrita em arquivos Excel.

Este módulo fornece a classe FileOperator para manipular planilhas.
"""

from __future__ import annotations

from contextlib import suppress
from typing import TYPE_CHECKING, cast

from pandas import DataFrame, ExcelWriter, concat, read_excel

if TYPE_CHECKING:
    from pathlib import Path

    from openpyxl import Workbook

    from backend.interfaces import DataSave


class FileOperator:
    """Gerencie operações de leitura e escrita em arquivos Excel.

    Esta classe oferece métodos para carregar, criar e salvar dados
    em arquivos Excel, facilitando a manipulação de planilhas.
    """

    @classmethod
    def load_writer(cls, arquivo_xlsx: Path) -> ExcelWriter:
        """Carregue ou crie um ExcelWriter para o arquivo informado.

        Args:
            arquivo_xlsx (Path): Caminho do arquivo Excel.

        Returns:
            ExcelWriter: Objeto para manipulação do arquivo Excel.

        """
        if arquivo_xlsx.exists():
            return ExcelWriter(
                arquivo_xlsx,
                engine="openpyxl",
                mode="a",
                if_sheet_exists="replace",
            )

        return ExcelWriter(arquivo_xlsx, engine="openpyxl")

    def save_file(self, data: DataSave, arquivo_xlsx: Path) -> None:
        """Salve dados em uma planilha Excel existente ou nova.

        Args:
            data (DataSave): Dados e nome da worksheet.
            arquivo_xlsx (Path): Caminho do arquivo Excel.

        """
        with suppress(Exception):
            df = DataFrame(data["data_save"])
            writer = self.load_writer(arquivo_xlsx)
            wb = cast("Workbook", writer.book)

            # Verifica se a worksheet já existe
            if data["worksheet"] in wb.sheetnames:
                df_xlsx = read_excel(
                    arquivo_xlsx,
                    engine="openpyxl",
                    sheet_name=data["worksheet"],
                )
                df = concat([
                    DataFrame(df_xlsx.to_dict(orient="records")),
                    DataFrame(data["data_save"]),
                ])

            df.to_excel(
                excel_writer=writer,
                sheet_name=data["worksheet"],
                index=False,
            )
            writer.close()
