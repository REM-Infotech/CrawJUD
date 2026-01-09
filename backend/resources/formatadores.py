"""Forneça funções utilitárias para formatar strings.

Este módulo contém funções para remover acentos e caracteres
especiais, tornando textos seguros para nomes de arquivos.
"""

from __future__ import annotations

import re
import secrets
import traceback
from datetime import datetime
from typing import TYPE_CHECKING
from unicodedata import combining, normalize

from pandas import Timestamp
from werkzeug.utils import secure_filename

if TYPE_CHECKING:
    from typings import Any


MAIOR_60_ANOS = "Maior que 60 anos (conforme Lei 10.741/2003)"
VER_RECURSO = "Clique aqui para visualizar os recursos relacionados"


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


def formata_msg(exc: Exception | None = None) -> str:
    """Formata mensagem de erro detalhada a partir de uma exceção fornecida ao bot.

    Args:
        exc (Exception | None): Exceção a ser formatada, se fornecida.

    Returns:
        str: Mensagem formatada contendo detalhes da exceção, se houver.

    """
    if exc:
        return "\n Exception: " + "\n".join(
            traceback.format_exception_only(exc),
        )

    return ""
