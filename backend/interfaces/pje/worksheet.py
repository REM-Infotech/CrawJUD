"""Dicionários para salvamento em planilha."""

from __future__ import annotations

from typing import TYPE_CHECKING, TypedDict

if TYPE_CHECKING:
    from datetime import datetime


class CapaPJe(TypedDict):
    """Defina os campos da capa do processo no padrão PJe.

    Args:
        ID_PJE (int): Identificador único do processo no PJE.
        LINK_CONSULTA (str): Link para consulta do processo.
        NUMERO_PROCESSO (str): Número do processo judicial.
        CLASSE (str): Classe do processo.
        SIGLA_CLASSE (str): Sigla da classe do processo.
        ORGAO_JULGADOR (str): Nome do órgão julgador.
        SIGLA_ORGAO_JULGADOR (str): Sigla do órgão julgador.
        DATA_DISTRIBUICAO (datetime): Data de distribuição.
        STATUS_PROCESSO (str): Status do processo.
        SEGREDO_JUSTICA (str): Indica segredo de justiça.

    """

    ID_PJE: int
    LINK_CONSULTA: str
    NUMERO_PROCESSO: str
    CLASSE: str
    SIGLA_CLASSE: str
    ORGAO_JULGADOR: str
    SIGLA_ORGAO_JULGADOR: str
    DATA_DISTRIBUICAO: datetime
    STATUS_PROCESSO: str
    SEGREDO_JUSTICA: str
