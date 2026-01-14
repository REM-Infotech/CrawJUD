from __future__ import annotations

from functools import wraps
from typing import TYPE_CHECKING, ParamSpec, overload

from quart_socketio import Namespace

if TYPE_CHECKING:
    from collections.abc import Callable

P = ParamSpec("P")


class BlueprintNamespace(Namespace):
    def __init__(self, namespace: str = "CrawJUD") -> None:
        super().__init__(namespace)

    @overload
    def on[T](self, event: str) -> Callable[[Callable[P, T]], Callable[P, T]]: ...

    @overload
    def on[T](self, event: str, handler: Callable[P, T]) -> Callable[P, T]: ...

    def on[T](
        self,
        event: str,
        handler: Callable[P, T] | None = None,
    ) -> Callable[P, T] | Callable[[Callable[P, T]], Callable[P, T]]:

        event_name = self._formata_nome_evento(event)
        if handler:
            return self._event_register(event_name, handler)

        def wrapped[T](fn: Callable[P, T]) -> Callable[P, T]:
            return self._event_register(event_name, fn)

        return wrapped

    def event[T](self, fn: Callable[P, T]) -> Callable[P, T]:

        event_name = self._formata_nome_evento(fn.__name__)
        return self._event_register(event_name, fn)

    def _event_register[T](self, event_name: str, fn: Callable[P, T]) -> Callable[P, T]:

        @wraps(fn)
        def wrapper[T](*args: P.args, **kwargs: P.kwargs) -> T:
            return fn(self, *args, **kwargs)

        setattr(self, event_name, wrapper)
        return wrapper

    @classmethod
    def _formata_nome_evento(cls, nome: str) -> str:

        event_name = nome

        if not event_name.startswith("on"):
            event_name = f"on_{event_name}"

        return event_name
