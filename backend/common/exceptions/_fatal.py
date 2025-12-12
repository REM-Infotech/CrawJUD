from traceback import format_exception
from typing import ClassVar, Self

type AnyType = any


class FatalError(Exception):
    """Exceção fatal na execução do bot CrawJUD."""

    message: ClassVar[str] = "Fatal error in CrawJUD bot execution."

    def __init__(
        self,
        exc: Exception,
        *args: AnyType,
        msg: str | None = None,
    ) -> None:
        """Initialize FatalError with the given exception.

        Args:
            exc (Exception): The exception that caused the fatal error.
            msg: Message (Optional)
            *args (AnyType): Additional arguments to pass to the base Exception.

        """
        if msg:
            self._msg = msg

        # Store only the string representation to ensure picklability
        self._exc_str = repr(exc)
        self._exc_type = type(exc).__name__
        self._exc_msg = str(exc)
        self._traceback = "".join(format_exception(exc))
        self._format()
        super().__init__(*args)

    def _format(self) -> None:
        self.message = self._traceback

    def __str__(self) -> str:
        """Return the string representation of the FatalError."""
        return self.message

    def __repr__(self) -> str:
        """Return the string representation of the FatalError for debugging."""
        return f"FatalException(type={self._exc_type}, message={self._exc_msg})"

    def __reduce__(self) -> tuple[type[Self], tuple[Exception]]:
        # Provide a way for pickle to reconstruct the object
        return (
            self.__class__,
            (Exception(self._exc_msg),),  # reconstruct with a generic Exception
        )

    def __getstate__(self) -> dict[str, AnyType]:
        # Only store pickleable attributes
        return {
            "_exc_str": self._exc_str,
            "_exc_type": self._exc_type,
            "_exc_msg": self._exc_msg,
            "_traceback": self._traceback,
            "message": self.message,
        }

    def __setstate__(self, state: dict[str, AnyType]) -> None:
        self._exc_str = state["_exc_str"]
        self._exc_type = state["_exc_type"]
        self._exc_msg = state["_exc_msg"]
        self._traceback = state["_traceback"]
        self.message = state["message"]
