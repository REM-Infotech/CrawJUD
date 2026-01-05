from __future__ import annotations

import json
from contextlib import suppress
from typing import TYPE_CHECKING, Any, ClassVar, Self

from backend.dicionarios import PartePJe, RepresentantePJe
from backend.resources.elements import pje as el

if TYPE_CHECKING:
    from httpx import Client


type AnyType = Any


class PartesPJe:
    representantes_unformatted: ClassVar[list[dict[int, dict[str, str]]]] = []
    partes_list: list[dict[str, str]]

    def __init__(self, partes: list[dict[str, str]], processo: str) -> None:
        self.partes_list = partes
        self.processo: str = processo
        self.representantes_unformatted = []

    @classmethod
    def extrair(
        cls,
        cliente: Client,
        regiao: str,
        id_processo: str,
        processo: str,
    ) -> Self | None:
        link_partes = el.LINK_CONSULTA_PARTES.format(
            trt_id=regiao,
            id_processo=id_processo,
        )

        processo: str = ""

        with suppress(Exception):
            request_partes = cliente.get(url=link_partes)
            if request_partes:
                return cls(partes=json.loads(request_partes.content), processo=processo)

        return None

    def formata_partes(
        self,
    ) -> list[PartePJe]:
        partes = []
        representantes_unformatted = []
        for pos, parte in enumerate(self.partes_list):
            partes.append(
                PartePJe(
                    ID_PJE=parte.get("id"),
                    NOME=parte.get("nome"),
                    DOCUMENTO=parte.get(
                        "documento",
                        "000.000.000-00",
                    ),
                    TIPO_DOCUMENTO=parte.get(
                        "tipoDocumento",
                        "Não Informado",
                    ),
                    TIPO_PARTE=parte.get("polo"),
                    TIPO_PESSOA="Física"
                    if parte.get("tipoPessoa", "f").lower() == "f"
                    else "Jurídica",
                    PROCESSO=self.processo,
                    POLO=parte.get("polo"),
                    PARTE_PRINCIPAL=parte.get("principal", False),
                ),
            )
            representantes = parte.get("representantes")
            if representantes:
                representantes_unformatted.append({pos, representantes})

        self.representantes_unformatted = representantes_unformatted
        return partes

    def formata_representantes(self) -> list[RepresentantePJe]:
        representantes: list[RepresentantePJe] = []
        for item in self.representantes_unformatted:
            pos, representante = next(iter(item.items()))
            parte = self.partes_list[int(pos)]

            processo = ""
            representantes.append(
                RepresentantePJe(
                    ID_PJE=representante.get("id", ""),
                    PROCESSO=processo,
                    NOME=representante.get("nome", ""),
                    DOCUMENTO=representante.get(
                        "documento",
                        "",
                    ),
                    TIPO_DOCUMENTO=representante.get(
                        "tipoDocumento",
                        "",
                    ),
                    REPRESENTADO=parte["nome"],
                    TIPO_PARTE=representante["polo"],
                    TIPO_PESSOA=representante["tipoPessoa"],
                    POLO=representante["polo"],
                    OAB=representante.get(
                        "numeroOab",
                        "0000",
                    ),
                    EMAILS=",".join(
                        representante.get("emails", []),
                    ),
                    TELEFONE=PartesPJe.__formata_numero_representante(representante),
                ),
            )

        return representantes

    @staticmethod
    def __formata_numero_representante(
        representante: AnyType,
    ) -> str:
        if "dddCelular" in representante and "numeroCelular" in representante:
            numero = representante.get("numeroCelular")
            ddd = representante.get("dddCelular")
            return f"({ddd}) {numero}"

        return ""
