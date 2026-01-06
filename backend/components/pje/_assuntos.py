from __future__ import annotations

from contextlib import suppress
from typing import TYPE_CHECKING

from backend.dicionarios import AssuntoPJe
from backend.resources.elements import pje as el

if TYPE_CHECKING:
    from httpx import Client


class AssuntosPJe:
    @classmethod
    def extrair(
        cls,
        *,
        cliente: Client,
        regiao: str,
        id_processo: str,
        processo: str,
        grau: int,
    ) -> list[AssuntoPJe]:
        link_assuntos = el.LINK_CONSULTA_ASSUNTOS.format(
            trt_id=regiao,
            id_processo=id_processo,
        )
        with suppress(Exception):
            request_assuntos = cliente.get(url=link_assuntos)
            if request_assuntos:
                return [
                    AssuntoPJe(
                        ID_PJE=assunto["id"],
                        NUMERO_PROCESSO=processo,
                        INSTANCIA=grau,
                        ASSUNTO_COMPLETO=assunto["assunto"]["assuntoCompleto"],
                        ASSUNTO_RESUMIDO=assunto["assunto"]["assuntoResumido"],
                    )
                    for assunto in request_assuntos.json()
                ]

        return []
