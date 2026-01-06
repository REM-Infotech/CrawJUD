from typing import TypeVar

from flask_sqlalchemy.extension import SQLAlchemy as Alchemy
from sqlalchemy.orm import DeclarativeBase, DeclarativeBaseNoMeta, DeclarativeMeta

from backend.base.sqlalchemy._model import Model
from backend.base.sqlalchemy._query import Query

_FSA_MCT = TypeVar(
    "_FSA_MCT",
    bound=type[Model] | DeclarativeMeta | type[DeclarativeBase] | type[DeclarativeBaseNoMeta],
)

class SQLAlchemy(Alchemy):
    Model: type[Model]
    Query: Query

    def _make_declarative_base(
        self,
        model_class: _FSA_MCT,
        disable_autonaming: bool = ...,
    ) -> type[Model]: ...
