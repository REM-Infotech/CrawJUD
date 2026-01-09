"""Módulo de controle de classes para os robôs."""

from backend.controllers import CrawJUD
from backend.controllers.csi import CsiBot
from backend.controllers.elaw import ElawBot
from backend.controllers.esaj import ESajBot
from backend.controllers.pje import PJeBot
from backend.controllers.projudi import ProjudiBot

__all__ = ["CrawJUD", "CsiBot", "ESajBot", "ElawBot", "PJeBot", "ProjudiBot"]
