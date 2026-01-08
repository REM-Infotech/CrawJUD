from collections.abc import Callable
from typing import TypedDict, Unpack, overload

from celery.app.amqp import AMQP
from celery.app.base import Celery as BaseCelery
from celery.app.control import Control
from celery.app.events import Events
from celery.app.log import Logging
from celery.app.registry import TaskRegistry
from celery.loaders.app import AppLoader

from backend.base.task import CeleryTask

class KwCelery(TypedDict):
    main: str
    loader: AppLoader
    control: type[Control]
    changes: dict
    autofinalize: bool
    namespace: str
    strict_typing: bool
    broker: str
    backend: str
    autofinalize: bool
    set_as_current: bool
    include: list[str]
    amqp: type[AMQP]
    events: type[Events]
    log: type[Logging]
    tasks: type[TaskRegistry]
    fixups: list[str]
    config_source: type
    task_cls: type[CeleryTask]

class Celery(BaseCelery):
    def __init__(self, **kwargs: Unpack[KwCelery]) -> None: ...

@overload
def shared_task[**P, T](
    name: str,
) -> Callable[[Callable[P, T]], CeleryTask[P, T]]: ...
@overload
def shared_task[**P, T](
    name: str,
    *,
    bind: bool,
) -> Callable[[Callable[P, T]], CeleryTask[P, T]]: ...
@overload
def shared_task[**P, T](
    name: str,
    *,
    bind: bool,
    base: CeleryTask,
) -> Callable[[Callable[P, T]], CeleryTask[P, T]]: ...
@overload
def shared_task[**P, T](fn: Callable[P, T]) -> CeleryTask[P, T]: ...
