"""Recursos da API."""

import re
import secrets
from string import ascii_uppercase, digits
from typing import LiteralString
from unicodedata import combining, normalize

from werkzeug.utils import secure_filename


def gerar_id() -> LiteralString:
    """Gere identificador aleatório de 8 caracteres alfanuméricos.

    Returns:
        LiteralString: ID com letras e números aleatórios.

    """
    # Define os caracteres possíveis para letras e números
    letters = ascii_uppercase
    numbers = digits

    id_chars = []
    # Gera 4 pares de letra e número para formar 8 caracteres
    for _ in range(4):
        id_chars.extend((secrets.choice(letters), secrets.choice(numbers)))

    # Junta os caracteres em uma única string
    return "".join(id_chars)


def camel_to_snake(name: str) -> str:
    """Convenção de uma string CamelCase para snake_case.

    Returns:
        str: String convertida para snake_case.

    """
    # Adiciona underscore antes de letras maiúsculas precedidas de minúsculas
    snake_case_step1 = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", name)
    # Adiciona underscore antes de letras maiúsculas precedidas de números ou minúsculas
    return re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", snake_case_step1).lower()


def formata_string(string: str) -> str:
    """Remova acentos e caracteres especiais da string.

    Args:
        string (str): Texto a ser formatado.

    Returns:
        str: Texto formatado em caixa alta e seguro para nomes
            de arquivo.

    """
    normalized_string = "".join([c for c in normalize("NFKD", string) if not combining(c)])

    return secure_filename(normalized_string)
