from __future__ import annotations

from typing import TypedDict


class AssuntoPJe(TypedDict):
    """Defina os campos dos assuntos do processo judicial no padrão PJe.

    Args:
        ID_PJE (int): Identificador único do processo no PJE.
        PROCESSO (str): Número do processo judicial.
        ASSUNTO_COMPLETO (str): Descrição completa do assunto.
        ASSUNTO_RESUMIDO (str): Descrição resumida do assunto.

    Returns:
        AssuntoPJe: Dicionário tipado com os dados dos assuntos.

    """

    ID_PJE: int
    PROCESSO: str
    ASSUNTO_COMPLETO: str
    ASSUNTO_RESUMIDO: str


class AudienciaProcessoPJe(TypedDict):
    """Defina os campos das audiências do processo no padrão PJe.

    Args:
        ID_PJE (int): Identificador único do processo no PJE.
        NUMERO_PROCESSO (str): Número do processo judicial.
        TIPO_AUDIENCIA (str): Tipo da audiência.
        MODO_AUDIENCIA (str): Modo de realização da audiência.
        STATUS (str): Status da audiência.
        DATA_INICIO (str): Data de início da audiência.
        DATA_FIM (str): Data de término da audiência.
        DATA_MARCACAO (str): Data de marcação da audiência.

    """

    ID_PJE: int
    NUMERO_PROCESSO: str
    TIPO_AUDIENCIA: str
    MODO_AUDIENCIA: str
    STATUS: str
    DATA_INICIO: str
    DATA_FIM: str
    DATA_MARCACAO: str


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


class RepresentantePJe(TypedDict):
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


__all__ = [
    "AssuntoPJe",
    "AudienciaProcessoPJe",
    "PartePJe",
    "RepresentantePJe",
]
