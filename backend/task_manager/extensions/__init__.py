"""Extensões do App."""

from __future__ import annotations

from contextlib import suppress
from typing import TYPE_CHECKING

from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from passlib.context import CryptContext

from backend.task_manager.base import Model, Query
from backend.task_manager.constants import WORKDIR as WORKDIR

if TYPE_CHECKING:
    from flask import Flask

db = SQLAlchemy(model_class=Model, query_class=Query)
mail = Mail()


crypt_context = CryptContext.from_string("""
[passlib]
schemes = argon2, bcrypt
default = argon2
deprecated = bcrypt
""")


def start_extensions(app: Flask) -> None:
    """Inicializa as extensões do Flask."""
    with app.app_context():
        with suppress(RuntimeError):
            if not app.extensions.get("sqlalchemy"):
                db.init_app(app)

        with suppress(RuntimeError):
            mail.init_app(app)
