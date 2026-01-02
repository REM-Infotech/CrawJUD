from __future__ import annotations

from ._main import BotData


class Protocolo(BotData):
    NUMERO_PROCESSO: str
    ANEXOS: str
    TIPO_PROTOCOLO: str
    TIPO_ARQUIVO: str
    TIPO_ANEXOS: str
    SUBTIPO_PROTOCOLO: str
    PETICAO_PRINCIPAL: str
    PARTE_PETICIONANTE: str


class ProjudiProtocolo(Protocolo): ...


class PJeProtocolo(Protocolo): ...


class EsajProtocolo(Protocolo): ...
