"""Defina funcionalidades dos bots do sistema.

Este pacote reúne módulos responsáveis por diferentes
operações automatizadas, como administração, busca,
cálculo, capa, emissão, intimações, movimentação e protocolo.
"""

import api.task_manager._hook as hook

from . import (
    admin,
    buscadores,
    calculadoras,
    capa,
    emissao,
    habilitacao,
    intimacoes,
    movimentacao,
    protocolo,
)

__all__ = [
    "admin",
    "buscadores",
    "calculadoras",
    "capa",
    "emissao",
    "habilitacao",
    "hook",
    "intimacoes",
    "movimentacao",
    "protocolo",
]
