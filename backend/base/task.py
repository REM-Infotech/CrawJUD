"""Fornece integração de tarefas Celery com contexto Flask."""

from __future__ import annotations

from celery import Task


class FlaskTask[**P, R](Task):
    """Integre tarefas Celery ao contexto Flask nesta classe."""

    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> R:
        """Executa a tarefa Celery dentro do contexto Flask.

        Args:
            *args (AnyType): Argumentos posicionais da tarefa.
            **kwargs (AnyType): Argumentos nomeados da tarefa.

        Returns:
            AnyType: Resultado da execução da tarefa.

        """
        return self.run(*args, **kwargs)

    async def _run(self, *args: P.args, **kwargs: P.kwargs) -> R:
        return await self.run(*args, **kwargs)
