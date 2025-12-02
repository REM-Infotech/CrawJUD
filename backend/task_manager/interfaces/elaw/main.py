"""Gerencie e manipule dados do eLaw com utilitários.

Este módulo fornece a classe ElawData para manipulação de dados
relacionados ao sistema eLaw, incluindo métodos para limpeza,
atualização e formatação de informações.

"""

from __future__ import annotations

from collections import UserDict
from typing import TYPE_CHECKING

from backend.task_manager.constants.data._bots.cidades import cidades_amazonas

if TYPE_CHECKING:
    from backend.task_manager.types_app import AnyType, Dict


class ElawData(UserDict):
    """Gerencie e manipule dados do eLaw com métodos utilitários."""

    def __init__(self, values: Dict | None = None, **kwargs: AnyType) -> None:
        """Inicialize a instância ElawData com dados fornecidos.

        Args:
            values (Dict | None): Dados iniciais do eLaw.
            **kwargs (AnyType): Argumentos adicionais.

        """
        super().__init__(values, **kwargs)

        self._remove_empty_keys()
        self._format_numeric_values()
        self._set_data_inicio()
        self._update_tipo_parte_contraria()
        self._update_capital_interior()

    def _remove_empty_keys(self) -> None:
        """Remove chaves com valores vazios ou None."""
        dict_data = self.data.copy()
        for key in dict_data:
            value = dict_data[key]
            if (isinstance(value, str) and not value.strip()) or value is None:
                self.data.pop(key)

    def _update_tipo_parte_contraria(self) -> None:
        """Atualize 'TIPO_PARTE_CONTRARIA' se 'TIPO_EMPRESA' for 'RÉU'."""
        tipo_empresa = self.data.get("TIPO_EMPRESA", "").upper()
        if tipo_empresa == "RÉU":
            self.data["TIPO_PARTE_CONTRARIA"] = "Autor"

    def _update_capital_interior(
        self,
    ) -> Dict[str, str]:
        """Atualize o campo 'CAPITAL_INTERIOR' conforme 'COMARCA'."""
        comarca = self.data.get("COMARCA")
        if comarca:
            set_locale = cidades_amazonas.get(comarca, "Outro Estado")
            self.data["CAPITAL_INTERIOR"] = set_locale

    def _set_data_inicio(self) -> Dict[str, str]:
        """Defina 'DATA_INICIO' se ausente e 'DATA_LIMITE' presente."""
        if "DATA_LIMITE" in self.data and not self.data.get("DATA_INICIO"):
            self.data["DATA_INICIO"] = self.data["DATA_LIMITE"]

    def _format_numeric_values(self) -> None:
        """Formata valores numéricos para duas casas decimais."""
        loop_data = self.data.items()
        for key, value in loop_data:
            if isinstance(value, (int, float)):
                self.data[key] = f"{value:.2f}".replace(".", ",")
