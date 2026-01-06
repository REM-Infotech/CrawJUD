"""Módulo de interfaces do task manager."""

from __future__ import annotations

from typing import Literal, TypedDict


class ColorsDict(TypedDict):
    """Dicionário de cores para mensagens do bot, conforme o padrão.

    Args:
        info (Literal["cyan"]): Cor para mensagens informativas.
        log (Literal["yellow"]): Cor para mensagens de log.
        error (Literal["red"]): Cor para mensagens de erro.
        warning (Literal["magenta"]): Cor para mensagens de aviso.
        success (Literal["green"]): Cor para mensagens de sucesso.

    Returns:
        TypedDict: Estrutura contendo os tipos de cores para cada
            mensagem.

    Raises:
        KeyError: Se uma das chaves obrigatórias estiver ausente.

    """

    info: Literal["cyan"]
    log: Literal["yellow"]
    error: Literal["red"]
    warning: Literal["magenta"]
    success: Literal["green"]
