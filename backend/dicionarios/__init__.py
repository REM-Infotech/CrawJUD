from __future__ import annotations

from typing import TYPE_CHECKING, TypedDict

from .api import HealtCheck, LoginForm
from .planilhas_robos import (
    BotData,
    ElawCondenacao,
    ElawCustas,
    ElawProvisionamento,
    EsajCapa,
    JusdsProvisionamento,
    PJeCapa,
    PJeMovimentacao,
    ProjudiCapa,
    ProjudiMovimentacao,
)
from .robos import (
    AssuntoPJe,
    AudienciaProcessoPJe,
    CapaPJe,
    DocumentoPJe,
    ExpedienteDocumentoPJe,
    MovimentacaoPJe,
    PartePJe,
    RepresentantePJe,
)

if TYPE_CHECKING:
    from typings import MessageType, StatusBot


class Message(TypedDict, total=False):
    """Defina estrutura para mensagens do bot."""

    pid: str
    message: str
    time_message: str
    message_type: MessageType
    status: StatusBot
    start_time: str
    row: int
    total: int
    erros: int
    sucessos: int
    restantes: int


__all__ = [
    "AssuntoPJe",
    "AudienciaProcessoPJe",
    "BotData",
    "CapaPJe",
    "DocumentoPJe",
    "ElawCondenacao",
    "ElawCustas",
    "ElawProvisionamento",
    "EsajCapa",
    "ExpedienteDocumentoPJe",
    "HealtCheck",
    "JusdsProvisionamento",
    "LoginForm",
    "Message",
    "MovimentacaoPJe",
    "PJeCapa",
    "PJeMovimentacao",
    "PartePJe",
    "ProjudiCapa",
    "ProjudiMovimentacao",
    "RepresentantePJe",
]
