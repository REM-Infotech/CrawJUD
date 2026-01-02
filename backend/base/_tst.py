from __future__ import annotations

import re
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from backend.types_app import AnyType


class CustomPattern:
    def __init__(self, pattern: str = "", flags: int = 0) -> None:
        self.raw_pattern = pattern
        self.flags = flags
        self._compiled = re.compile(pattern, flags)

    def match(self, text: str) -> re.Match[str] | None:
        return self._compiled.match(text)

    def search(self, text: str) -> re.Match[str] | None:
        return self._compiled.search(text)

    def fullmatch(self, text: str) -> re.Match[str] | None:
        return self._compiled.fullmatch(text)

    def findall(self, text: str) -> list[AnyType]:
        return self._compiled.findall(text)

    def sub(self, repl: str, text: str) -> str:
        return self._compiled.sub(repl, text)

    def __repr__(self) -> str:
        return f"<CustomPattern pattern={self.raw_pattern!r}>"
