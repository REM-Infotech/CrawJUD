from __future__ import annotations

from typing import ClassVar

from backend.controllers import PJeBot


class HabilitacaoPJe(PJeBot):
    name: ClassVar[str] = "pje_habilitacao"
