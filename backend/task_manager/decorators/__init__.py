"""Fornece decoradores para tarefas compartilhadas com Celery."""

from __future__ import annotations

import asyncio
from asyncio import iscoroutine
from importlib import import_module
from typing import TYPE_CHECKING

from celery import shared_task
from dynaconf import FlaskDynaconf
from flask import Flask, current_app

from backend.base import FlaskTask

if TYPE_CHECKING:
    from collections.abc import Callable

    from backend.task_manager.proto import CeleryTask
    from backend.types_app import AnyType, P


def import_class(path: str) -> object:
    """Importa e retorne uma classe a partir do caminho informado.

    Args:
        path (str): Caminho completo da classe.

    Returns:
        object: Classe importada dinamicamente.

    """
    module_path, class_name = path.rsplit(".", 1)
    module = import_module(module_path)
    return getattr(module, class_name)


class SharedClassMethodTask:
    """Defina decorador para criar tarefas Celery de classmethods.

    Args:
        name (str): Nome da tarefa.
        bind (bool): Se deve vincular a instância.
        base (object | None): Classe base da tarefa.

    """

    def __init__(
        self,
        name: str,
        *,
        bind: bool = False,
        base: object | None = None,
    ) -> None:
        """Inicialize o decorador com nome, bind e base da tarefa.

        Args:
            name (str): Nome da tarefa.
            bind (bool): Se deve vincular a instância.
            base (object | None): Classe base da tarefa.

        """
        self._name = name
        self._bind = bind
        self._base = base or FlaskTask

    def __call__[T](self, fn: Callable[P, T]) -> CeleryTask[P, T]:
        """Decora classmethod como tarefa Celery compartilhada.

        Args:
            fn (Callable[P, T]): Classmethod a ser decorado.

        Returns:
            CeleryTask[P, T]: Tarefa Celery decorada.

        """
        self._path_cls = f"{fn.__module__}.{fn.__qualname__.split('.')[0]}"
        self.has_app = "app" in fn.__annotations__
        self._fn = fn
        decorar = shared_task(name=self._name, bind=self._bind, base=self._base)
        return decorar(self._run)

    def _run[T](
        self,
        *args: AnyType,
        **kwargs: AnyType,
    ) -> T:
        """Executa o classmethod decorado, suportando async.

        Args:
            cls: Classe do classmethod.
            *args (AnyType): Argumentos posicionais.
            **kwargs (AnyType): Argumentos nomeados.

        Returns:
            T: Resultado do classmethod.

        """
        from backend.config import settings

        _kwarg = kwargs
        _arg = args
        is_async = iscoroutine(self._fn)
        cls = import_class(self._path_cls)
        app = Flask(__name__)

        FlaskDynaconf(
            app=app,
            instance_relative_config=True,
            extensions_list="EXTENSIONS",  # pyright: ignore[reportArgumentType]
            dynaconf_instance=settings,
            env="api",
        )

        with app.app_context():
            if self.has_app:
                kwargs.update({"app": current_app})

            if is_async:
                return asyncio.run(
                    self._fn(cls, *args, **kwargs),
                )
            return self._fn(cls, *args, **kwargs)


class SharedTask:
    """Defina decorador para criar tarefas compartilhadas com Celery.

    Args:
        name (str): Nome da tarefa.
        bind (bool): Se deve vincular a instância.
        base (object | None): Classe base da tarefa.

    """

    def __init__(
        self,
        name: str,
        *,
        bind: bool = False,
        base: object | None = None,
    ) -> None:
        """Inicialize o decorador com nome, bind e base da tarefa.

        Args:
            name (str): Nome da tarefa.
            bind (bool): Se deve vincular a instância.
            base (object | None): Classe base da tarefa.

        """
        self._name = name
        self._bind = bind
        self._base = base or FlaskTask

    def __call__[T](self, fn: Callable[P, T]) -> CeleryTask[P, T]:
        """Decora função como tarefa Celery compartilhada.

        Args:
            fn (Callable[P, T]): Função a ser decorada.

        Returns:
            CeleryTask[P, T]: Tarefa Celery decorada.

        """
        self._fn = fn
        decorar = shared_task(name=self._name, bind=self._bind, base=self._base)
        return decorar(self._run)

    def _run[T](self, *args: AnyType, **kwargs: AnyType) -> T:
        is_async = iscoroutine(self._fn)
        if is_async:
            return asyncio.run(self._fn(*args, **kwargs))

        return self._fn(*args, **kwargs)
