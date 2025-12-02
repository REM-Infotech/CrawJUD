"""Bases customizadas para classes de Extensões e Modelos."""

from api.base._sqlalchemy._model import Model
from api.base._sqlalchemy._query import Query

__all__ = ["Model", "Query"]
