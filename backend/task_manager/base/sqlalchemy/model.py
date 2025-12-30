"""Forneça utilitários para integração com SQLAlchemy.

Inclui classes para manipular instâncias e nomes de tabelas dinamicamente.
"""

from __future__ import annotations

from contextlib import suppress
from typing import TYPE_CHECKING, ClassVar, Self, cast

from flask import current_app
from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy.model import Model as FSA_Model

from backend.resources import camel_to_snake

from .query import Query, QueryProperty

if TYPE_CHECKING:
    from backend.types_app import AnyType


class FSAProperty:
    """Gerencie a instância do SQLAlchemy de forma dinâmica.

    Atributos:
        fsa_instante (SQLAlchemy): Instância do SQLAlchemy.
    """

    fsa_instante: SQLAlchemy = SQLAlchemy()

    def __set__(self, *args, **kwargs) -> None:
        """Defina dinamicamente a instância do SQLAlchemy."""
        self.fsa_instante = args[1]

    def __get__(self, *args, **kwargs) -> SQLAlchemy:
        """Obtenha dinamicamente a instância do SQLAlchemy.

        Args:
            *args (tuple): Argumentos posicionais.
            **kwargs (dict): Argumentos nomeados.

        Returns:
            SQLAlchemy: Instância atual do SQLAlchemy.

        """
        with suppress(KeyError):
            app = current_app
            with app.app_context():
                if "sqlalchemy" in app.extensions:
                    db: SQLAlchemy = app.extensions["sqlalchemy"]
                    self.fsa_instante = db

        return self.fsa_instante


class FSATableName:
    """Gerencie dinamicamente o nome da tabela SQLAlchemy.

    Atributos:
        _tablename (str): Nome da tabela em snake_case.
    """

    _tablename: ClassVar[str] = ""

    def __set__(self, *args) -> None:
        """Defina dinamicamente o nome da tabela."""
        self._tablename = args[1]  # pyright: ignore[reportAttributeAccessIssue]

    def __get__(
        self,
        cls: Model | None = None,
        *args: AnyType,
        **kwargs: AnyType,
    ) -> str:
        """Retorne dinamicamente o nome da tabela em snake_case.

        Args:
            cls (Model | None): Classe do modelo.
            *args (AnyType): Argumentos posicionais.
            **kwargs (AnyType): Argumentos nomeados.

        Returns:
            str: Nome da tabela em snake_case.

        """
        if cls:
            snake_cased = camel_to_snake(cls.__class__.__name__)
            cls.__name__ = cls.__tablename__ or snake_cased  # pyright: ignore[reportAttributeAccessIssue]

        return self._tablename


class Model(FSA_Model):
    """Implemente modelo base para integração com SQLAlchemy."""

    query: ClassVar[Query[Self]] = cast("Query[Self]", QueryProperty())  # pyright: ignore[reportIncompatibleVariableOverride]
    __fsa__: ClassVar[SQLAlchemy] = cast("SQLAlchemy", FSAProperty())
    __tablename__: ClassVar[str] = FSAProperty()
