"""Log bot."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flask_jwt_extended import jwt_required

from backend.api.routes._blueprints import fileNS

from .upload import uploader

if TYPE_CHECKING:
    from backend.base import BlueprintNamespace
    from typings import Any as Any


@fileNS.on("add_file")
@jwt_required()
def add_file(self: BlueprintNamespace, data: Any = None) -> None:
    """Log bot."""
    uploader(data)
