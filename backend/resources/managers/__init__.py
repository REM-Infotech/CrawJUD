"""Defina gerenciadores de recursos para bots.

Este pacote fornece módulos para gerenciar credenciais e arquivos.
"""

from .credencial_manager import CredencialManager
from .file_manager import FileManager

__all__ = ["CredencialManager", "FileManager"]
