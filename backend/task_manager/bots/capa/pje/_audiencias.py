from __future__ import annotations

from contextlib import suppress
from typing import TYPE_CHECKING, TypedDict

from backend.task_manager.resources.elements import pje as el

if TYPE_CHECKING:
    from httpx import Client


class AudienciasProcessos(TypedDict):
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


class InformacoesAudiencias:
    @classmethod
    def audiencias(cls, regiao: str, id_processo: str, cliente: Client) -> None:
        link_audiencias = el.LINK_AUDIENCIAS.format(
            trt_id=regiao,
            id_processo=id_processo,
        )
        processo: str = ""
        with suppress(Exception):
            request_audiencias = cliente.get(url=link_audiencias)
            if request_audiencias:
                return cls._formata_audiencias(
                    processo=processo,
                    data_audiencia=request_audiencias.json(),
                )

        return {}

    @classmethod
    def _formata_audiencias(
        cls,
        processo: str,
        data_audiencia: list[dict],
    ) -> list[AudienciasProcessos]:
        return [
            AudienciasProcessos(
                ID_PJE=audiencia["id"],
                processo=processo,
                TIPO_AUDIENCIA=audiencia["tipo"]["descricao"],
                MODO_AUDIENCIA="PRESENCIAL"
                if audiencia["tipo"]["isVirtual"]
                else "VIRTUAL",
                STATUS=audiencia["status"],
                DATA_INICIO=audiencia.get("dataInicio"),
                DATA_FIM=audiencia.get("dataFim"),
                DATA_MARCACAO=audiencia.get("dataMarcacao"),
            )
            for audiencia in data_audiencia
        ]
