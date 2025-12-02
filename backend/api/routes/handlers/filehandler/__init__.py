"""Log bot."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flask_jwt_extended import jwt_required

from backend.api.extensions import io
from backend.api.routes.handlers.filehandler.upload import uploader

if TYPE_CHECKING:
    from backend.api.types_app import AnyType


@io.on("add_file", namespace="/files")
@jwt_required()
def add_file(data: AnyType = None) -> None:
    """Log bot."""
    uploader(data)
