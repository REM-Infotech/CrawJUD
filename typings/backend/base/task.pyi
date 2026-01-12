from celery import Celery
from celery.app.task import Task

type Any = any

class CeleryTask(Task):
    app: Celery
    def __call__(self, *args: Any, **kwargs: Any) -> Any: ...
    async def _run(self, *args: Any, **kwargs: Any) -> Any: ...
