"""Gerencie rotas principais e registro de blueprints da aplicação.

Este módulo define rotas básicas e integra blueprints de autenticação e bots.
"""

from ._routes import register_routes

__all__ = ["register_routes"]
