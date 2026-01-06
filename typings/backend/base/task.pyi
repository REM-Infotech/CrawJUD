from typing import Self

from celery.app.task import Task

class FlaskTask[**P, R](Task):
    run: Self[P, R]

    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> R: ...
    async def _run(self, *args: P.args, **kwargs: P.kwargs) -> R: ...
