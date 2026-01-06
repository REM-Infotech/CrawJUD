from backend.common.exceptions import BaseCrawJUDError

type AnyType = any


class ArquivoNaoEncontradoError(BaseCrawJUDError):
    def __init__(
        self,
        caminho: str,
        message: str = "",
        exc: Exception | None = None,
    ) -> None:

        self._caminho_arquivo = caminho
        self.repr_exc = repr(exc)
        super().__init__(message, exc)

    def __str__(self) -> str:
        return self._caminho_arquivo

    def __repr__(self) -> str:

        caminho = self._caminho_arquivo
        msg = self.message
        repr_ = self.repr_exc
        return f"ArquivoNaoEncontradoError<caminho={caminho}, message={msg}, exc={repr_}>"

    def __getstate__(self) -> dict[str, str]:
        return {
            "_caminho_arquivo": str(self._caminho_arquivo),
            "message": str(self.message),
            "repr_exc": str(self.repr_exc),
        }

    def __setstate__(self, state: AnyType) -> None:
        self._caminho_arquivo = state["_caminho_arquivo"]
        self.message = state["message"]
        self.repr_exc = state["repr_exc"]
        self.exc = state.get("exc", None)
