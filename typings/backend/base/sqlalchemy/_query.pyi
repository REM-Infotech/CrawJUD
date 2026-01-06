from collections.abc import Sequence
from typing import ClassVar, Self

from flask_sqlalchemy.pagination import Pagination as FSAPagination
from flask_sqlalchemy.pagination import (
    QueryPagination as FSAQueryPagination,
)
from sqlalchemy.orm import Query as SAQuery
from sqlalchemy.sql._typing import (
    _ColumnExpressionArgument,
    _ColumnsClauseArgument,
)

type Any = any
type Entities[T] = _ColumnsClauseArgument[T] | Sequence[_ColumnsClauseArgument[T]]

class QueryProperty[T]:
    def __init__(self) -> None: ...
    def __get__(self, instance: Any, owner: type[T]) -> Query[T]: ...

class Pagination[T](FSAPagination): ...
class QueryPagination[T](FSAQueryPagination): ...

class Query[T](SAQuery):
    _total: ClassVar[int] = 0

    def len(self) -> int: ...
    @property
    def total(self) -> int: ...
    @total.setter
    def total(self, new_total: int) -> None: ...
    def filter(self, *criterion: _ColumnExpressionArgument) -> Self: ...
    def filter_by(self, **kwargs: Any) -> Self: ...
    def first(self) -> T | None: ...
    def all(self) -> list[T]: ...
    def get_or_404(
        self,
        ident: Any,
        description: str | None = None,
    ) -> T: ...
    def first_or_404(self, description: str | None = None) -> T: ...
    def one_or_404(self, description: str | None = None) -> T: ...
    def paginate(
        self,
        *,
        page: int | None = None,
        per_page: int | None = None,
        max_per_page: int | None = None,
        error_out: bool = True,
        count: bool = True,
    ) -> QueryPagination[T]: ...
