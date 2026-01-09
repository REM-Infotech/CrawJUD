"""Módulo de controle dos robôs de raspagem de capa."""

from .esaj import Capa as EsajCapaTask
from .pje import Capa as PJeCapaTask
from .projudi import Capa as ProjudiCapaTask

__all__ = ["EsajCapaTask", "PJeCapaTask", "ProjudiCapaTask"]
