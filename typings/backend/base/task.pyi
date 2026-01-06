from collections.abc import Callable

from celery.app.task import Task

class FlaskTask[**P, R](Task):
    run: Callable[P, R]

    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> R: ...
    async def _run(self, *args: P.args, **kwargs: P.kwargs) -> R: ...
