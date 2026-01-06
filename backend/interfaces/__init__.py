"""Módulo de interfaces do task manager."""

from __future__ import annotations

from typing import TYPE_CHECKING, Literal, TypedDict

from .datasheet import BotData

if TYPE_CHECKING:
    from typings import (
        MessageType,
        Sistemas,
        StatusBot,
    )


class DictUsers(TypedDict):
    Id: int
    login: str
    nome_usuario: str
    email: str
    password: str
    login_time: str
    verification_code: str
    login_id: str
    filename: str
    blob_doc: bytes
    licenseus_id: int


class DictCredencial(TypedDict):
    Id: int
    nome_credencial: str
    system: Sistemas
    login_metodo: str
    login: str
    password: str


class DataSave(TypedDict):
    """Estrutura para salvar dados do bot em planilhas do sistema.

    Args:
        worksheet (str): Nome da planilha onde os dados serão salvos.
        data_save (list[BotData]): Lista de dados do bot a serem
            armazenados.

    Returns:
        TypedDict: Estrutura contendo nome da planilha e dados do bot.

    Raises:
        KeyError: Se uma das chaves obrigatórias estiver ausente.

    """

    worksheet: str
    data_save: list[BotData]


class Message(TypedDict, total=False):
    """Defina estrutura para mensagens do bot."""

    pid: str
    message: str
    time_message: str
    message_type: MessageType
    status: StatusBot
    start_time: str
    row: int
    total: int
    erros: int
    sucessos: int
    restantes: int


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


class DataSucesso(TypedDict):
    """Defina estrutura para dados de sucesso do bot.

    Args:
        NUMERO_PROCESSO (str): Número do processo.
        MENSAGEM (str): Mensagem de sucesso.
        NOME_COMPROVANTE (str): Nome do comprovante.
        NOME_COMPROVANTE_2 (str): Nome do segundo comprovante.

    """

    NUMERO_PROCESSO: str
    MENSAGEM: str
    NOME_COMPROVANTE: str
    NOME_COMPROVANTE_2: str


__all__ = ["BotData"]
