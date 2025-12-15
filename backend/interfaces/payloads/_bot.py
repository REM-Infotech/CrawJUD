from __future__ import annotations

from typing import TYPE_CHECKING, TypedDict

if TYPE_CHECKING:
    from backend.types_app.payloads import ConfigForm, SystemBots


class BotInfo(TypedDict):
    Id: int
    configuracao_form: ConfigForm
    display_name: str
    sistema: SystemBots
    descricao: str
    categoria: str
