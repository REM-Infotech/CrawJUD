"""Inicialize o pacote de extensões do sistema CrawJUD.

Este módulo permite o uso de integrações e extensões como MinIO,
banco de dados, autenticação e outros recursos compartilhados.
"""

from .extensions import (
    app,
    celery,
    cors,
    create_app,
    crypt_context,
    db,
    io,
    jwt,
    keepass,
    mail,
    make_celery,
    storage,
)

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
