# ruff: noqa: D105

"""Módulo para controle de exceptions de validações de valores."""

from __future__ import annotations

from traceback import format_exception
from typing import Self

type Any = any


class ValidacaoStringError(ValueError):
    """Exception de erro de validação de string."""

    message: str
    exception: ValueError

    def __init__(self, *args: Any, message: str) -> None:
        """Inicializa exception de validação."""
        super().__init__(*args)
        self.message = message
        self.exception = self
        self._traceback = "\n".join(format_exception(self))

    def _format(self) -> None:
        self.message = self._traceback

    def __str__(self) -> str:
        """Return the string representation of the FatalError."""
        return self.message

    def __repr__(self) -> str:
        """Return the string representation of the FatalError for debugging."""
        return f"ValidacaoStringError(type={self._exc_type}, message={self._exc_msg})"

    def __reduce__(self) -> tuple[type[Self], tuple[Exception]]:
        # Provide a way for pickle to reconstruct the object
        return (
            self.__class__,
            (Exception(self._exc_msg),),  # reconstruct with a generic Exception
        )

    def __getstate__(self) -> dict[str, Any]:
        # Only store pickleable attributes
        return {
            "_exc_str": self._exc_str,
            "_exc_type": self._exc_type,
            "_exc_msg": self._exc_msg,
            "_traceback": self._traceback,
            "message": self.message,
        }

    def __setstate__(self, state: dict[str, Any]) -> None:
        self._exc_str = state["_exc_str"]
        self._exc_type = state["_exc_type"]
        self._exc_msg = state["_exc_msg"]
        self._traceback = state["_traceback"]
        self.message = state["message"]
