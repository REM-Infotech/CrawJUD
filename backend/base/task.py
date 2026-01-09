"""Fornece integração de tarefas Celery com contexto Flask."""

from __future__ import annotations

from typing import TYPE_CHECKING

from celery.app.task import Task

if TYPE_CHECKING:
    from collections.abc import Callable


class CeleryTask[**P, R](Task):
    """Integre tarefas Celery ao contexto Flask nesta classe."""

    run: Callable[P, R]

    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> R:
        """Executa a tarefa Celery dentro do contexto Flask.

        Args:
            *args (Any): Argumentos posicionais da tarefa.
            **kwargs (Any): Argumentos nomeados da tarefa.

        Returns:
            Any: Resultado da execução da tarefa.

        """
        return self.run(*args, **kwargs)

    async def _run(self, *args: P.args, **kwargs: P.kwargs) -> R:
        return await self.run(*args, **kwargs)
