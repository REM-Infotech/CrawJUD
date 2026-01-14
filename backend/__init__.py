"""Inicie a aplicação Quart e o servidor SocketIO.

Este script é o ponto de entrada principal para a API. Ele cria a aplicação,
carrega as rotas e executa o servidor SocketIO na porta definida.
"""

from . import _hook as hook
from ._main import typerapp

__all__ = ["hook", "typerapp"]
