from dataclasses import dataclass

from backend.api._forms.head import FormBot


@dataclass(match_args=False)
class OnlyFile(FormBot):
    bot_id: str
    xlsx: str
