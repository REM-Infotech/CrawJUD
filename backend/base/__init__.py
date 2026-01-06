"""Bases customizadas para classes de Extensões e Modelos."""

from backend.base.sqlalchemy._model import Model
from backend.base.sqlalchemy._query import Query

from ._socketio import BlueprintNamespace
from .task import CeleryTask

__all__ = ["BlueprintNamespace", "CeleryTask", "Model", "Query"]
