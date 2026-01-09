"""Defina funcionalidades dos bots do sistema.

Este pacote reúne módulos responsáveis por diferentes
operações automatizadas, como administração, busca,
cálculo, capa, emissão, intimações, movimentação e protocolo.
"""

from .capa import EsajCapaTask, PJeCapaTask, ProjudiCapaTask

__all__ = [
    "EsajCapaTask",
    "PJeCapaTask",
    "ProjudiCapaTask",
]
