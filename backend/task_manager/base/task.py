"""Fornece integração de tarefas Celery com contexto Flask."""

from __future__ import annotations

from typing import TYPE_CHECKING

from celery import Task

if TYPE_CHECKING:
    from backend.task_manager.types_app import AnyType


class FlaskTask(Task):
    """Integre tarefas Celery ao contexto Flask nesta classe."""

    def __call__(self, *args: AnyType, **kwargs: AnyType) -> AnyType:
        """Executa a tarefa Celery dentro do contexto Flask.

        Args:
            *args (AnyType): Argumentos posicionais da tarefa.
            **kwargs (AnyType): Argumentos nomeados da tarefa.

        Returns:
            AnyType: Resultado da execução da tarefa.

        """
        return self.run(*args, **kwargs)

    async def _run(self, *args, **kwargs) -> AnyType:
        return await self.run(*args, **kwargs)
