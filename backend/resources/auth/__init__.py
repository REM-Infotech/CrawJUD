"""Módulo de controle de classes de autenticação."""

from .elaw import AutenticadorElaw
from .jusds import AutenticadorJusds
from .pje import AutenticadorPJe
from .projudi import AutenticadorProjudi

__all__ = [
    "AutenticadorElaw",
    "AutenticadorJusds",
    "AutenticadorPJe",
    "AutenticadorProjudi",
]
