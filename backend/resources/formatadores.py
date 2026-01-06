"""Forneça funções utilitárias para formatar strings.

Este módulo contém funções para remover acentos e caracteres
especiais, tornando textos seguros para nomes de arquivos.
"""

from __future__ import annotations

import secrets
from datetime import datetime
from unicodedata import combining, normalize

from pandas import Timestamp
from werkzeug.utils import secure_filename


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


def random_base36() -> str:
    """Gere string aleatória em base 36 para identificadores.

    Returns:
        str: Valor aleatório em base 36 como string.

    """
    # Gera um número aleatório de 52 bits (mesma entropia de Math.random)
    random_number = secrets.randbits(52)
    chars = "0123456789abcdefghijklmnopqrstuvwxyz"
    result = ""
    while random_number:
        random_number, remainder = divmod(random_number, 36)
        result = chars[remainder] + result
    return "0." + result or "0.0"


def normalizar(txt: str) -> str:
    """Normalize espaços em branco em uma string.

    Args:
        txt (str): Texto a ser normalizado.

    Returns:
        str: Texto com espaços simples entre palavras.

    """
    return " ".join(txt.split())


def format_data(value: Any) -> str:
    """Formata datas ou valores nulos para string legível.

    Args:
        value (Any): Valor a ser formatado.

    Returns:
        str: Data formatada ou string vazia se nulo.

    """
    if str(value) == "NaT" or str(value) == "nan":
        return ""

    if isinstance(value, (datetime, Timestamp)):
        return value.strftime("%d/%m/%Y")

    return value


def format_float(value: Any) -> str:
    """Formata número float para string com duas casas decimais.

    Args:
        value (Any): Número a ser formatado.

    Returns:
        str: Número formatado com vírgula como separador decimal.

    """
    return f"{value:.2f}".replace(".", ",")
