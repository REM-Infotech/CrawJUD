from __future__ import annotations

import json
from contextlib import suppress
from typing import TYPE_CHECKING, ClassVar, Literal, Self, cast

from backend.dicionarios import PartePJe, RepresentantePJe
from backend.resources.elements import pje as el

if TYPE_CHECKING:
    from httpx import Client


type Any = any
type PartesList = list[dict[str, str]]
type PartesPorPolos = dict[
    Literal["ATIVO", "PASSIVO", "OUTROS"],
    PartesList,
]


class PartesPJe:
    representantes_unformatted: ClassVar[
        list[dict[int, list[dict[str, str]]]]
    ] = []
    partes_list: PartesList

    def __init__(
        self,
        partes: list[dict[str, str]],
        processo: str,
        grau: int,
    ) -> None:
        self.partes_list = partes
        self.processo: str = processo
        self.representantes_unformatted = []
        self.grau = grau

    @classmethod
    def extrair(
        cls,
        *,
        cliente: Client,
        regiao: str,
        id_processo: str,
        processo: str,
        grau: int,
    ) -> Self | None:
        link_partes = el.LINK_CONSULTA_PARTES.format(
            trt_id=regiao,
            id_processo=id_processo,
        )
        with suppress(Exception):
            request_partes = cliente.get(url=link_partes)
            if request_partes:
                return cls(
                    partes=json.loads(request_partes.content),
                    processo=processo,
                    grau=grau,
                )

        return None

    def formata_partes(
        self,
    ) -> list[PartePJe]:
        partes = []
        representantes_unformatted = []

        if isinstance(self.partes_list, dict):
            partes_polos = cast("PartesPorPolos", self.partes_list)
            partes_formatted = []
            for v in list(partes_polos.values()):
                partes_formatted.extend(v)

            self.partes_list = partes_formatted

        for pos, parte in enumerate(self.partes_list):
            partes.append(
                PartePJe(
                    NUMERO_PROCESSO=self.processo,
                    INSTANCIA=self.grau,
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
                    POLO=parte.get("polo"),
                    PARTE_PRINCIPAL=parte.get("principal", False),
                ),
            )
            representantes = parte.get("representantes")
            if representantes:
                representantes_unformatted.append({pos: representantes})

        self.representantes_unformatted = representantes_unformatted
        return partes

    def formata_representantes(self) -> list[RepresentantePJe]:
        representantes: list[RepresentantePJe] = []
        for item in self.representantes_unformatted:
            pos, representantes_list = next(iter(item.items()))
            parte = self.partes_list[int(pos)]

            representantes.extend(
                RepresentantePJe(
                    ID_PJE=representante.get("id", ""),
                    NUMERO_PROCESSO=self.processo,
                    INSTANCIA=self.grau,
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
                    TELEFONE=PartesPJe.__formata_numero_representante(
                        representante,
                    ),
                )
                for representante in representantes_list
            )

        return representantes

    @staticmethod
    def __formata_numero_representante(
        representante: Any,
    ) -> str:
        if (
            "dddCelular" in representante
            and "numeroCelular" in representante
        ):
            numero = representante.get("numeroCelular")
            ddd = representante.get("dddCelular")
            return f"({ddd}) {numero}"

        return ""
