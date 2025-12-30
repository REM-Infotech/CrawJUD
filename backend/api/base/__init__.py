"""Bases customizadas para classes de Extensões e Modelos."""

from backend.api.base._sqlalchemy._model import Model
from backend.api.base._sqlalchemy._query import Query

from ._socketio import BlueprintNamespace

__all__ = ["BlueprintNamespace", "Model", "Query"]
