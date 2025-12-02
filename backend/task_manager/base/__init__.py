"""Bases customizadas para classes de Extensões e Modelos."""

from .sqlalchemy.model import Model
from .sqlalchemy.query import Query
from .task import FlaskTask

__all__ = ["FlaskTask", "Model", "Query"]
