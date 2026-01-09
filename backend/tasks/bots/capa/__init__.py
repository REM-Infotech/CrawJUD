"""Módulo de controle dos robôs de raspagem de capa."""

from .pje import Capa as PJeCapaTask
from .projudi import Capa as ProjudiCapaTask

__all__ = ["PJeCapaTask", "ProjudiCapaTask"]
