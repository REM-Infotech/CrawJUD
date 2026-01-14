"""Fornece integração de tarefas Celery com contexto Quart."""

from __future__ import annotations

from asyncio import Runner, iscoroutinefunction
from typing import TYPE_CHECKING

from celery.app.task import Task

if TYPE_CHECKING:
    from collections.abc import Callable

    from celery import Celery


class CeleryTask[**P, R](Task):
    """Integre tarefas Celery ao contexto Quart nesta classe."""

    run: Callable[P, R]
    app: Celery

    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> R:
        """Executa a tarefa Celery dentro do contexto Quart.

        Args:
            *args (Any): Argumentos posicionais da tarefa.
            **kwargs (Any): Argumentos nomeados da tarefa.

        Returns:
            Any: Resultado da execução da tarefa.

        """
        if iscoroutinefunction(self.run):
            with Runner() as runner:
                return runner.run(self._run(*args, **kwargs))

        return self.run(*args, **kwargs)

    async def _run(self, *args: P.args, **kwargs: P.kwargs) -> R:
        return await self.run(*args, **kwargs)
