from __future__ import annotations

from contextlib import suppress
from typing import TYPE_CHECKING, TypedDict

from backend.task_manager.resources.elements import pje as el

if TYPE_CHECKING:
    from httpx import Client


class Assuntos(TypedDict):
    """Defina os campos dos assuntos do processo judicial no padrão PJe.

    Args:
        ID_PJE (int): Identificador único do processo no PJE.
        PROCESSO (str): Número do processo judicial.
        ASSUNTO_COMPLETO (str): Descrição completa do assunto.
        ASSUNTO_RESUMIDO (str): Descrição resumida do assunto.

    Returns:
        Assuntos: Dicionário tipado com os dados dos assuntos.

    """

    ID_PJE: int
    PROCESSO: str
    ASSUNTO_COMPLETO: str
    ASSUNTO_RESUMIDO: str


class AssuntosPJe:
    @classmethod
    def assuntos(
        cls,
        cliente: Client,
        regiao: str,
        id_processo: str,
    ) -> list[Assuntos]:
        link_assuntos = el.LINK_CONSULTA_ASSUNTOS.format(
            trt_id=regiao,
            id_processo=id_processo,
        )
        processo: str = ""
        with suppress(Exception):
            request_assuntos = cliente.get(url=link_assuntos)
            if request_assuntos:
                return [
                    Assuntos(
                        ID_PJE=assunto["id"],
                        PROCESSO=processo,
                        ASSUNTO_COMPLETO=assunto["assunto"]["assuntoCompleto"],
                        ASSUNTO_RESUMIDO=assunto["assunto"]["assuntoResumido"],
                    )
                    for assunto in request_assuntos.json()
                ]

        return [{}]
