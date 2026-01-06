"""Constantes do sistema."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typings import Sistemas

SISTEMAS: set[Sistemas] = {
    "projudi",
    "elaw",
    "esaj",
    "pje",
    "jusds",
    "csi",
}
