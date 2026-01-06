from __future__ import annotations

from contextlib import suppress
from typing import TYPE_CHECKING, ClassVar, Self, cast

from flask import current_app
from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy.model import Model as FSA_Model

from backend.api.resources import camel_to_snake

from ._query import Query, QueryProperty

if TYPE_CHECKING:
    from typings import Any

type Any = any


class FSAProperty:
    fsa_instante: SQLAlchemy = SQLAlchemy()

    def __set__(self, *args: Any, **kwargs: Any) -> None:
        self.fsa_instante = args[1]

    def __get__(self, *args: Any, **kwargs: Any) -> SQLAlchemy:
        with suppress(KeyError):
            app = current_app
            with app.app_context():
                if "sqlalchemy" in app.extensions:
                    db: SQLAlchemy = app.extensions["sqlalchemy"]
                    self.fsa_instante = db

        return self.fsa_instante


class FSATableName:
    _tablename: ClassVar[str] = ""

    def __set__(self, *args: Any) -> None:
        self._tablename = args[1]  # pyright: ignore[reportAttributeAccessIssue]

    def __get__(
        self,
        cls: Model | None = None,
        *args: Any,
        **kwargs: Any,
    ) -> str:
        if cls:
            snake_cased = camel_to_snake(cls.__class__.__name__)
            cls.__name__ = cls.__tablename__ or snake_cased  # pyright: ignore[reportAttributeAccessIssue]

        return self._tablename


class Model(FSA_Model):
    query: ClassVar[Query[Self]] = cast("Query[Self]", QueryProperty())  # pyright: ignore[reportIncompatibleVariableOverride]
    __fsa__: ClassVar[SQLAlchemy] = cast("SQLAlchemy", FSAProperty())
    __tablename__: ClassVar[str] = FSAProperty()

    def to_dict(self) -> dict:

        data = {}
        for item in filter(
            lambda x: not x.startswith("_") and x != "query",
            dir(self),
        ):
            value = getattr(self, item, None)

            if isinstance(value, list):
                value: list[Self]
                val_list = [it.to_dict() for it in value]
                value: list[dict[str, str]] = val_list

            data.update({item: value})

        return data
