"""Defina interfaces para dados do Projudi.

Este pacote contém dicionários tipados para estruturar
informações de processos, partes e representantes do Projudi.
"""

from __future__ import annotations

from typing import TypedDict


class CapaProjudiDict(TypedDict):
    """Defina o dicionário para dados da capa do processo Projudi.

    Args:
        NUMERO_PROCESSO (str): Número do processo.
        COMARCA (str): Comarca do processo.
        COMPETENCIA (str): Competência do processo.
        JUIZO (str): Juízo responsável.
        JUIZ (str): Nome do juiz.
        OBJETO_PEDIDO (str): Objeto do pedido.
        CLASSIFICACAO_PROCESSUAL (str): Classificação processual.
        SITUACAO (str): Situação do processo.
        SEQUENCIAL (str): Sequencial do processo.
        INTERVENCAO_DO_MP (str): Intervenção do MP.
        VALOR_DA_CAUSA (str): Valor da causa.
        STATUS (str): Status do processo.
        CLASSE_PROCESSUAL (str): Classe processual.
        ASSUNTO_PRINCIPAL (str): Assunto principal.
        NIVEL_DE_SIGILO (str): Nível de sigilo.

    """

    NUMERO_PROCESSO: str = ""
    COMARCA: str = ""
    COMPETENCIA: str = ""
    JUIZO: str = ""
    JUIZ: str = ""
    OBJETO_PEDIDO: str = ""
    CLASSIFICACAO_PROCESSUAL: str = ""
    SITUACAO: str = ""
    SEQUENCIAL: str = ""
    INTERVENCAO_DO_MP: str = ""
    VALOR_DA_CAUSA: str = ""
    STATUS: str = ""
    CLASSE_PROCESSUAL: str = ""
    ASSUNTO_PRINCIPAL: str = ""
    NIVEL_DE_SIGILO: str = ""


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
