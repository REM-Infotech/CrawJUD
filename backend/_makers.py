"""CrawJUD - Sistema de Automação Jurídica."""

from __future__ import annotations

from celery import Celery
from celery.signals import after_setup_logger
from dotenv import load_dotenv
from dynaconf import FlaskDynaconf
from flask import Flask
from passlib.context import CryptContext
from werkzeug.middleware.proxy_fix import ProxyFix

from backend import _hook
from backend.base import CeleryTask
from backend.config import CeleryConfig, settings
from backend.resources import setup_logger

__name__ = "CrawJUD"

celery_app = Celery(__name__, task_cls=CeleryTask)
after_setup_logger.connect(setup_logger)
app: Flask = Flask(__name__)
load_dotenv()

crypt_context: CryptContext = CryptContext.from_string("""
[passlib]
schemes = argon2, bcrypt
default = argon2
deprecated = bcrypt
""")


def make_celery(app: Flask) -> Celery:
    """Create and configure a Celery instance with Quart application context.

    Returns:
        Celery: Configured Celery instance.

    """
    from backend.tasks.register import register_tasks

    celery_app.config_from_object(CeleryConfig(app.config))
    celery_app.set_default()
    app.extensions["celery"] = celery_app

    register_tasks()

    return celery_app


"""Inicialize a aplicação Flask principal da API CrawJUD.

Este módulo configura a aplicação, carrega variáveis de ambiente,
define o contexto de criptografia e fornece a função de criação da app.
"""


def create_app() -> Flask:
    """Crie e configure a aplicação Flask.

    Returns:
        Flask: Instância configurada da aplicação Flask.

    """
    # Configura a aplicação com Dynaconf
    FlaskDynaconf(
        app=app,
        instance_relative_config=True,
        dynaconf_instance=settings,
        extensions_list="EXTENSIONS",
    )

    # Adiciona middleware para corrigir headers de proxy reverso
    app.wsgi_app = ProxyFix(
        app.wsgi_app,
        x_for=1,
        x_proto=1,
        x_host=1,
        x_prefix=1,
    )
    return app


__all__ = ["_hook", "app", "celery_app", "crypt_context", "make_celery", "settings"]
