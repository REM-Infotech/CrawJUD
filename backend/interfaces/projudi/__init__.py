"""Defina interfaces para dados do Projudi.

Este pacote contém dicionários tipados para estruturar
informações de processos, partes e representantes do Projudi.
"""

from __future__ import annotations

from typing import TypedDict


class PartesProjudiDict(TypedDict):
    """Defina o dicionário para partes do processo Projudi.

    Args:
        NUMERO_PROCESSO (str): Número do processo.
        NOME (str): Nome da parte.
        DOCUMENTO (str): Documento da parte.
        CPF_CNPJ (str): CPF ou CNPJ da parte.
        ADVOGADOS (str): Advogados da parte.
        ENDERECO (str): Endereço da parte.

    """

    NUMERO_PROCESSO: str = ""
    NOME: str = ""
    DOCUMENTO: str = ""
    CPF_CNPJ: str = ""
    ADVOGADOS: str = ""
    ENDERECO: str = ""


class RepresentantesProjudiDict(TypedDict):
    """Defina o dicionário para representantes do Projudi.

    Args:
        NUMERO_PROCESSO (str): Número do processo.
        NOME (str): Nome do representante.
        OAB (str): OAB do representante.
        REPRESENTADO (str): Nome do representado.

    """

    NUMERO_PROCESSO: str = ""
    NOME: str = ""
    OAB: str = ""
    REPRESENTADO: str = ""
