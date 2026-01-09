"""Módulo de controle dos robôs de raspagem de capa."""

from .esaj import Movimentacao as EsajMovimentacaoTask
from .pje import Movimentacao as PJeMovimentacaoTask
from .projudi import Movimentacao as ProjudiMovimentacaoTask

__all__ = ["EsajMovimentacaoTask", "PJeMovimentacaoTask", "ProjudiMovimentacaoTask"]
