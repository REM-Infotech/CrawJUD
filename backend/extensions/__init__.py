"""Extensões do App."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from celery import Celery
from flask.app import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_keepass import KeepassManager
from flask_mail import Mail
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from passlib.context import CryptContext
from socketio.redis_manager import RedisManager

from backend.api.base import Model, Query
from backend.api.base._tst import CustomPattern
from backend.extensions._minio import Minio

if TYPE_CHECKING:
    from dynaconf.contrib import DynaconfConfig
    from flask import Flask

celery = Celery(__name__)
db = SQLAlchemy(model_class=Model, query_class=Query)  # pyright: ignore[reportArgumentType]
jwt = JWTManager()
mail = Mail()
io = SocketIO()
cors = CORS()
storage = Minio()
keepass = KeepassManager()

crypt_context: CryptContext = CryptContext.from_string("""
[passlib]
schemes = argon2, bcrypt
default = argon2
deprecated = bcrypt
""")

__all__ = ["CustomPattern", "cors", "db", "jwt", "mail", "start_extensions"]


def start_extensions(app: Flask) -> Flask:
    """Inicializa as extensões do Flask."""
    with app.app_context():
        if not app.extensions.get("sqlalchemy"):
            db.init_app(app)

        jwt.init_app(app)
        mail.init_app(app)
        io.init_app(
            app,
            json=app.json,
            async_mode="threading",
            cors_allowed_origins="*",
            client_manager=RedisManager(app.config["BROKER_URL"]),
        )
        cors.init_app(
            app,
            supports_credentials=True,
        )

        storage.init_app(app)

        Path(app.config["KEEPASS_FILENAME"]).parent.mkdir(parents=True, exist_ok=True)

        keepass.init_app(app)

        class CeleryConfig:
            def __init__(self, values: DynaconfConfig) -> None:
                for k, v in list(values.items()):
                    if str(k).isupper():
                        setattr(self, k, v)

        celery.config_from_object(CeleryConfig(app.config))
        celery.conf.update(
            worker_hijack_root_logger=False,
            worker_redirect_stdouts=False,
            worker_redirect_stdouts_level="CRITICAL",
        )

    return app
