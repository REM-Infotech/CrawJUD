from __future__ import annotations

from dataclasses import dataclass

from backend.api._forms.head import FormBot


@dataclass(match_args=False)
class MultipleFiles(FormBot):
    bot_id: str
    credencial: str
    xlsx: str
    anexos: list[str]
