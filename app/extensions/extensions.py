from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import quart_flask_patch as quart_flask_patch
from celery import Celery
from dynaconf import FlaskDynaconf
from flask_jwt_extended import JWTManager
from flask_keepass import KeepassManager
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from quart import Quart
from quart_socketio import SocketIO
from socketio import RedisManager

from backend.config import settings

if TYPE_CHECKING:
    from dynaconf.contrib import DynaconfConfig


__name__ = "crawjud"
app = Quart(__name__)


celery = Celery(__name__)
db = SQLAlchemy()
jwt = JWTManager()
mail = Mail()
keepass = KeepassManager()
sio = SocketIO()
db = SQLAlchemy()


async def create_app() -> Quart:
    from app.routes import register_routes

    FlaskDynaconf(
        app=app,
        instance_relative_config=True,
        dynaconf_instance=settings,
    )

    await start_extensions(app)
    await register_routes(app)

    return app


async def start_extensions(app: Quart) -> Quart:

    async with app.app_context():
        if not app.extensions.get("sqlalchemy"):
            db.init_app(app)

        jwt.init_app(app)
        mail.init_app(app)
        sio.init_app(
            app,
            json=app.json,
            cors_allowed_origins="*",
            client_manager=RedisManager(app.config["BROKER_URL"]),
        )

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
