from __future__ import annotations

import json
from contextlib import suppress
from typing import TYPE_CHECKING, Any, ClassVar, TypedDict

from backend.resources.elements import pje as el

if TYPE_CHECKING:
    from httpx import Client


type AnyType = Any


class PartePJe(TypedDict):
    """Defina os campos das partes do processo judicial no padrão PJe.

    Args:
        ID_PJE (int): Identificador único do processo no PJE.
        NOME (str): Nome da parte.
        DOCUMENTO (str): Documento da parte.
        TIPO_DOCUMENTO (str): Tipo do documento.
        TIPO_PARTE (str): Tipo da parte (autor/réu).
        TIPO_PESSOA (str): Tipo da pessoa (física/jurídica).
        PROCESSO (str): Número do processo.
        POLO (str): Polo da parte (ativo/passivo).
        PARTE_PRINCIPAL (bool): Indica se é parte principal.

    """

    ID_PJE: int
    NOME: str
    DOCUMENTO: str
    TIPO_DOCUMENTO: str
    TIPO_PARTE: str
    TIPO_PESSOA: str
    PROCESSO: str
    POLO: str
    PARTE_PRINCIPAL: bool


class Representantes(TypedDict):
    """Defina os campos dos representantes das partes no padrão PJe.

    Args:
        ID_PJE (int): Identificador único do processo no PJE.
        NOME (str): Nome do representante.
        DOCUMENTO (str): Documento do representante.
        TIPO_DOCUMENTO (str): Tipo do documento.
        REPRESENTADO (str): Nome da parte representada.
        TIPO_PARTE (str): Tipo da parte representada.
        TIPO_PESSOA (str): Tipo da pessoa (física/jurídica).
        PROCESSO (str): Número do processo.
        POLO (str): Polo da parte (ativo/passivo).
        OAB (str): Número da OAB do representante.
        EMAILS (str): E-mails do representante.
        TELEFONE (str): Telefone do representante.

    Returns:
        Representantes: Dicionário tipado com dados do representante.

    """

    ID_PJE: int
    NOME: str
    DOCUMENTO: str
    TIPO_DOCUMENTO: str
    REPRESENTADO: str
    TIPO_PARTE: str
    TIPO_PESSOA: str
    PROCESSO: str
    POLO: str
    OAB: str
    EMAILS: str
    TELEFONE: str


class PartesPJe:
    representantes_unformatted: ClassVar[list[dict[int, dict[str, str]]]] = []
    partes_list: list[dict[str, str]]

    @staticmethod
    def __formata_numero_representante(
        representante: AnyType,
    ) -> str:
        if "dddCelular" in representante and "numeroCelular" in representante:
            numero = representante.get("numeroCelular")
            ddd = representante.get("dddCelular")
            return f"({ddd}) {numero}"

        return ""

    def __init__(self, partes: list[dict[str, str]], processo: str) -> None:
        self.partes_list = partes
        self.processo: str = processo
        self.representantes_unformatted = []

    @classmethod
    def partes(
        cls,
        cliente: Client,
        regiao: str,
        id_processo: str,
        processo: str,
    ) -> None:
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
        request_partes: list[dict[str, str]],
        processo: str,
    ) -> list[PartePJe]:
        partes = []
        representantes_unformatted = []
        for pos, parte in enumerate(request_partes):
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
                    PROCESSO=processo,
                    POLO=parte.get("polo"),
                    PARTE_PRINCIPAL=parte.get("principal", False),
                ),
            )

            if parte.get("representantes"):
                representantes = parte.get("representantes")
                representantes_unformatted.append({pos, representantes})

        self.representantes_unformatted = representantes_unformatted
        return partes

    def formata_representantes(self) -> list[Representantes]:
        representantes: list[Representantes] = []
        for item in self.representantes_unformatted:
            pos, representante = next(iter(item.items()))
            parte = self.partes_list[int(pos)]

            processo = ""
            representantes.append(
                Representantes(
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
