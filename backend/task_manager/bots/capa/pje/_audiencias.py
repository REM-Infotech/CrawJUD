from __future__ import annotations

from contextlib import suppress
from typing import TYPE_CHECKING

from backend.dicionarios import AudienciaProcessoPJe
from backend.resources.elements import pje as el

if TYPE_CHECKING:
    from httpx import Client


class AudienciasPJe:
    @classmethod
    def extrair(
        cls,
        *,
        cliente: Client,
        regiao: str,
        id_processo: str,
        processo: str,
        grau: int,
    ) -> list[AudienciaProcessoPJe]:
        link_audiencias = el.LINK_AUDIENCIAS.format(
            trt_id=regiao,
            id_processo=id_processo,
        )
        with suppress(Exception):
            request_audiencias = cliente.get(url=link_audiencias)
            if request_audiencias:
                return cls._formata_audiencias(
                    processo=processo,
                    data_audiencia=request_audiencias.json(),
                    grau=grau,
                )

        return []

    @classmethod
    def _formata_audiencias(
        cls,
        processo: str,
        data_audiencia: list[dict],
        grau: int,
    ) -> list[AudienciaProcessoPJe]:
        return [
            AudienciaProcessoPJe(
                ID_PJE=audiencia["id"],
                NUMERO_PROCESSO=processo,
                INSTANCIA=grau,
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
