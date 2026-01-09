"""Inicialize a aplicação Flask principal da API CrawJUD.

Este módulo configura a aplicação, carrega variáveis de ambiente,
define o contexto de criptografia e fornece a função de criação da app.
"""

from ._create_app import create_app

__all__ = ["create_app"]
