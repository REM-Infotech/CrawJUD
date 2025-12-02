"""Módulo de controle de classes para os robôs."""

from backend.task_manager.controllers.csi import CsiBot
from backend.task_manager.controllers.elaw import ElawBot
from backend.task_manager.controllers.esaj import ESajBot
from backend.task_manager.controllers.pje import PJeBot
from backend.task_manager.controllers.projudi import ProjudiBot

__all__ = ["CsiBot", "ESajBot", "ElawBot", "PJeBot", "ProjudiBot"]
