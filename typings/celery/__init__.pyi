from collections.abc import Callable
from typing import overload

from celery.app.base import Celery as BaseCelery

from backend.base.task import FlaskTask

class Celery(BaseCelery): ...

@overload
def shared_task[**P, T](
    name: str,
) -> Callable[[Callable[P, T]], FlaskTask[P, T]]: ...
@overload
def shared_task[**P, T](
    name: str,
    *,
    bind: bool,
) -> Callable[[Callable[P, T]], FlaskTask[P, T]]: ...
@overload
def shared_task[**P, T](
    name: str,
    *,
    bind: bool,
    base: FlaskTask,
) -> Callable[[Callable[P, T]], FlaskTask[P, T]]: ...
@overload
def shared_task[**P, T](fn: Callable[P, T]) -> FlaskTask[P, T]: ...
