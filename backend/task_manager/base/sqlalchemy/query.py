"""Implemente consultas tipadas e paginação para SQLAlchemy.

Fornece classes e utilitários para facilitar consultas tipadas,
paginação e integração com Flask-SQLAlchemy.
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING, ClassVar, Self, cast

from flask import abort, current_app
from flask_sqlalchemy.pagination import Pagination as FSAPagination
from flask_sqlalchemy.pagination import (
    QueryPagination as FSAQueryPagination,
)
from sqlalchemy import exc as sa_exc
from sqlalchemy.orm import Query as SAQuery
from sqlalchemy.sql._typing import (
    _ColumnExpressionArgument,
    _ColumnsClauseArgument,
)

from backend.types_app import AnyType, T

_Entities = _ColumnsClauseArgument[T] | Sequence[_ColumnsClauseArgument[T]]


if TYPE_CHECKING:
    from flask_sqlalchemy import SQLAlchemy

    from .model import Model


class QueryProperty[T]:
    """Forneça acesso ao objeto Query tipado para o modelo.

    Args:
        instance (AnyType): Instância do modelo.
        owner (type[T]): Classe do modelo.

    """

    def __init__(self) -> None:
        """Inicialize a propriedade de consulta para o modelo."""

    def __get__(self, instance: AnyType, owner: type[T]) -> Query[T]:
        """Retorne a consulta tipada para o modelo solicitado.

        Args:
            instance (AnyType): Instância do modelo.
            owner (type[T]): Classe do modelo.

        Returns:
            Query[T]: Consulta tipada para o modelo.

        """
        app = current_app
        cls = cast("Model", owner)
        if "sqlalchemy" in app.extensions:
            cls.__fsa__ = cast(
                "SQLAlchemy",
                app.extensions["sqlalchemy"],
            )  # pyright: ignore[reportAttributeAccessIssue]

        _owner = owner

        with app.app_context():
            return Query(cls, cls.__fsa__.session())


class Pagination[T](FSAPagination):
    """Adds typing to Flask-SQLAlchemy's Pagination."""


class QueryPagination[T](FSAQueryPagination):
    """Adds typing to Flask-SQLAlchemy's QueryPagination."""


class Query[T](SAQuery):
    """Dummy class to represent the Query type with a generic parameter."""

    _total: ClassVar[int] = 0

    def len(self) -> int:
        """Retorne o total de itens encontrados na consulta.

        Returns:
            int: Total de itens encontrados na consulta.

        """
        return self._total

    @property
    def total(self) -> int:
        """Obtenha o total de itens encontrados na consulta."""
        return self._total

    @total.setter
    def total(self, new_total: int) -> None:
        self._total = new_total

    def filter(self, *criterion: _ColumnExpressionArgument) -> Self:
        """Filtre a consulta usando critérios fornecidos.

        Returns:
            Self: Consulta filtrada conforme os critérios.

        """
        return super().filter(*criterion)

    def filter_by(self, **kwargs: AnyType) -> Self:
        """Filtre a consulta usando campos e valores fornecidos.

        Returns:
            Self: Consulta filtrada conforme os campos e valores.

        """
        return super().filter_by(**kwargs)

    def first(self) -> T | None:
        """Retorne o primeiro resultado encontrado ou None.

        Returns:
            T | None: Primeiro resultado ou None se não houver.

        """
        self._total = 1
        return super().first()

    def all(self) -> list[T]:
        """Retorne todos os resultados encontrados na consulta.

        Returns:
            list[T]: Lista de todos os resultados encontrados.

        """
        all_results = super().all()
        self._total = len(all_results)

        return all_results

    def get_or_404(self, ident: AnyType, description: str | None = None) -> T:
        """Recupere item pelo id ou retorne erro 404.

        Args:
            ident (AnyType): Identificador do item.
            description (str | None): Mensagem de erro opcional.

        Returns:
            T: Item encontrado ou aborta com 404.

        """
        rv = self.get(ident)

        if rv is None:
            abort(404, description=description)

        self._total = 1
        return rv

    def first_or_404(self, description: str | None = None) -> T:
        """Retorne o primeiro resultado ou aborte com erro 404.

        Args:
            description (str | None): Mensagem de erro opcional.

        Returns:
            T: Primeiro resultado encontrado ou aborta com 404.

        """
        rv = self.first()

        if rv is None:
            abort(404, description=description)

        self._total = 1
        return rv

    def one_or_404(self, description: str | None = None) -> T:
        """Retorne um resultado ou aborte com erro 404.

        Args:
            description (str | None): Mensagem de erro opcional.

        Returns:
            T: Resultado encontrado ou aborta com 404.

        """
        try:
            self._total = 1
            return self.one()
        except sa_exc.NoResultFound, sa_exc.MultipleResultsFound:
            abort(404, description=description)

    def paginate(
        self,
        *,
        page: int | None = None,
        per_page: int | None = None,
        max_per_page: int | None = None,
        error_out: bool = True,
        count: bool = True,
    ) -> QueryPagination[T]:
        """Paginar resultados da consulta conforme parâmetros fornecidos.

        Args:
            page (int | None): Número da página.
            per_page (int | None): Itens por página.
            max_per_page (int | None): Máximo de itens por página.
            error_out (bool): Se deve lançar erro ao falhar.
            count (bool): Se deve contar total de itens.

        Returns:
            QueryPagination[T]: Objeto de paginação da consulta.

        """
        return cast(
            "QueryPagination[Self]",
            QueryPagination(
                query=self,
                page=page,
                per_page=per_page,
                max_per_page=max_per_page,
                error_out=error_out,
                count=count,
            ),
        )
