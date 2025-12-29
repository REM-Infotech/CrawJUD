"""Pacote público para recursos do sistema.

Contém arquivos e utilitários de recursos compartilhados.
"""

import re

from backend.task_manager.constants import MAIOR_60_ANOS, VER_RECURSO

from .auth.pje import AutenticadorPJe
from .formatadores import formata_string
from .iterators.pje import RegioesIterator

__all__ = [
    "AutenticadorPJe",
    "RegioesIterator",
    "formata_string",
]


def camel_to_snake(name: str) -> str:
    """Converta string CamelCase para snake_case.

    Args:
        name (str): String no formato CamelCase.

    Returns:
        str: String convertida para snake_case.

    """
    # Adiciona underscore antes de letras maiúsculas precedidas de minúsculas
    snake_case_step1 = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", name)
    # Adiciona underscore antes de letras maiúsculas precedidas de números ou minúsculas
    return re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", snake_case_step1).lower()


def value_check(label: str, valor: str) -> bool:
    """Verifique se valor não está em constantes proibidas.

    Args:
        label (str): Rótulo do campo.
        valor (str): Valor a ser verificado.

    Returns:
        bool: True se valor for permitido, senão False.

    """
    # Verifica se o valor não contém ":" e não está nas constantes
    if label and valor and ":" not in valor:
        return valor not in {MAIOR_60_ANOS, VER_RECURSO}

    return False
