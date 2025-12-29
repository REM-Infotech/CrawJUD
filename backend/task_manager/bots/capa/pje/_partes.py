from __future__ import annotations

from contextlib import suppress
from typing import TYPE_CHECKING, Any, TypedDict

from backend.resources.elements import pje as el

if TYPE_CHECKING:
    from httpx import Client


type AnyType = Any


class Partes(TypedDict):
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
    @staticmethod
    def __formata_numero_representante(
        representante: AnyType,
    ) -> str:
        if "dddCelular" in representante and "numeroCelular" in representante:
            numero = representante.get("numeroCelular")
            ddd = representante.get("dddCelular")
            return f"({ddd}) {numero}"

        return ""

    @classmethod
    def partes(cls, cliente: Client, regiao: str, id_processo: str) -> None:
        link_partes = el.LINK_CONSULTA_PARTES.format(
            trt_id=regiao,
            id_processo=id_processo,
        )

        processo: str = ""

        with suppress(Exception):
            request_partes = cliente.get(url=link_partes)
            if request_partes:
                data_partes, data_representantes = self._salva_partes(
                    processo=processo,
                    data_partes=request_partes.json(),
                )

    @classmethod
    def formata_partes(cls, request_partes: list[dict[str, str]]) -> None:
        partes = []
        representantes_unformatted = []
        for parte in request_partes:
            partes.append(
                Partes(
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
                representantes_unformatted.extend(representantes)

    @classmethod
    def formata_representantes(cls, unformatted: list[dict[str, str]]) -> None:
        representantes: list[Representantes] = []
        for representante in unformatted:
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
                    TELEFONE=__formata_numero_representante(representante),
                ),
            )
