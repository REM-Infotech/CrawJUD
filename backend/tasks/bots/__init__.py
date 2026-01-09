"""Defina funcionalidades dos bots do sistema.

Este pacote reúne módulos responsáveis por diferentes
operações automatizadas, como administração, busca,
cálculo, capa, emissão, intimações, movimentação e protocolo.
"""

from .capa import EsajCapaTask, PJeCapaTask, ProjudiCapaTask
from .intimacoes import ProjudiIntimacoesTask
from .movimentacao import EsajMovimentacaoTask, PJeMovimentacaoTask, ProjudiMovimentacaoTask
from .provisionamento import JusdsProvisionamentoTask

__all__ = [
    "EsajCapaTask",
    "EsajMovimentacaoTask",
    "JusdsProvisionamentoTask",
    "PJeCapaTask",
    "PJeMovimentacaoTask",
    "ProjudiCapaTask",
    "ProjudiIntimacoesTask",
    "ProjudiMovimentacaoTask",
]
