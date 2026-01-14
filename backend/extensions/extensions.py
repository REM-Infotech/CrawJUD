"""Extensões do App."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import quart_flask_patch as quart_flask_patch
from celery import Celery
from celery.signals import after_setup_logger
from dotenv import load_dotenv
from dynaconf import FlaskDynaconf
from flask_jwt_extended import JWTManager
from flask_keepass import KeepassManager
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from passlib.context import CryptContext
from quart import Quart
from quart_cors import CORS
from quart_socketio import SocketIO

from backend.base import CeleryTask, Model, Query
from backend.config import CeleryConfig, settings
from backend.extensions._minio import Minio
from backend.resources import setup_logger

if TYPE_CHECKING:
    from dynaconf.contrib import DynaconfConfig


__name__ = "crawjud"

app: Quart = Quart(__name__)
celery = Celery(__name__, task_cls=CeleryTask)
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

after_setup_logger.connect(setup_logger)

load_dotenv()


def make_celery(app: Quart) -> Celery:
    """Create and configure a Celery instance with Quart application context.

    Returns:
        Celery: Configured Celery instance.

    """
    from backend.tasks.register import register_tasks

    celery.config_from_object(CeleryConfig(app.config))
    celery.set_default()
    app.extensions["celery"] = celery

    register_tasks()

    return celery


async def create_app() -> Quart:
    """Crie e configure a aplicação Quart.

    Returns:
        Quart: Instância configurada da aplicação Quart.

    """
    from backend.api.routes import register_routes

    # Configura a aplicação com Dynaconf
    FlaskDynaconf(
        app=app,
        instance_relative_config=True,
        dynaconf_instance=settings,
    )

    # Adiciona middleware para corrigir headers de proxy reverso
    await start_extensions(app)
    await register_routes(app)

    return app


async def start_extensions(app: Quart) -> Quart:
    """Inicializa as extensões do Quart."""
    async with app.app_context():
        if not app.extensions.get("sqlalchemy"):
            db.init_app(app)

        jwt.init_app(app)
        mail.init_app(app)
        io.init_app(app)
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

        app.extensions["celery"] = celery

    return app


__all__ = [
    "app",
    "celery",
    "cors",
    "create_app",
    "crypt_context",
    "db",
    "io",
    "jwt",
    "keepass",
    "mail",
    "make_celery",
    "storage",
]
