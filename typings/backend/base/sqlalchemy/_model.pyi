from typing import ClassVar, Self

from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy.model import Model as FSA_Model

from ._query import Query

type Any = any

class FSAProperty:
    fsa_instante: SQLAlchemy = ...

    def __set__(self, *args: Any, **kwargs: Any) -> None: ...
    def __get__(self, *args: Any, **kwargs: Any) -> SQLAlchemy: ...

class FSATableName:
    _tablename: ClassVar[str] = ""

    def __set__(self, *args: Any) -> None: ...
    def __get__(
        self,
        cls: Model | None = None,
        *args: Any,
        **kwargs: Any,
    ) -> str: ...

class Model(FSA_Model):
    query: ClassVar[Query[Self]] = ...
    __fsa__: ClassVar[SQLAlchemy] = ...
    __tablename__: ClassVar[str] = ...

    def to_dict(self) -> dict: ...
