"""Módulo de controle de classes para os robôs."""

from backend.controllers.csi import CsiBot
from backend.controllers.elaw import ElawBot
from backend.controllers.esaj import ESajBot
from backend.controllers.pje import PJeBot
from backend.controllers.projudi import ProjudiBot

__all__ = ["CsiBot", "ESajBot", "ElawBot", "PJeBot", "ProjudiBot"]
