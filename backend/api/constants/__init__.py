"""Constantes do sistema."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from api.types_app import Sistemas

SISTEMAS: set[Sistemas] = {
    "projudi",
    "elaw",
    "esaj",
    "pje",
    "jusds",
    "csi",
}
