"""Extração de informações de processos no Projudi.

Este pacote contém classes e funções para automatizar a
coleta de dados processuais do sistema Projudi.
"""

from __future__ import annotations

from typing import ClassVar

from backend.controllers import ProjudiBot

CONTAGEM = 300


class BuscaProcessual(ProjudiBot):
    name: ClassVar[str] = "busca_processual_projudi"

    def execution(self) -> None:

        print("ok")
