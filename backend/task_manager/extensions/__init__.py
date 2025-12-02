"""Extensões do App."""

from __future__ import annotations

from contextlib import suppress

from flask import Flask
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from passlib.context import CryptContext

from backend.task_manager.base import Model, Query
from backend.task_manager.constants import WORKDIR as WORKDIR

flaskapp = Flask(__name__)
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
    with app.app_context(), suppress(RuntimeError):
        db.init_app(app)
        mail.init_app(app)
