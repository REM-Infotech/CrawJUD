from __future__ import annotations

from typing import TYPE_CHECKING, TypedDict

from .api import HealtCheck, LoginForm
from .planilhas_robos import (
    BotData,
    ElawCondenacao,
    ElawCustas,
    ElawProvisionamento,
    EsajCapa,
    JusdsProvisionamento,
    PJeCapa,
    PJeMovimentacao,
    ProjudiCapa,
    ProjudiMovimentacao,
)
from .robos import (
    AssuntoPJe,
    AudienciaProcessoPJe,
    CapaPJe,
    DocumentoPJe,
    ElawData,
    ExpedienteDocumentoPJe,
    MovimentacaoPJe,
    PartePJe,
    PartesProjudiDict,
    RepresentantePJe,
    RepresentantesProjudiDict,
)

if TYPE_CHECKING:
    from typings import Dict, MessageType, Sistemas, StatusBot


class Message(TypedDict, total=False):
    """Defina estrutura para mensagens do bot."""

    id_execucao: str
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
    sistema: Sistemas
    login_metodo: str
    login: str
    password: str


class DictResults(TypedDict):
    id_processo: str
    data_request: Dict


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


class Credencial(TypedDict):
    username: str
    password: str
    otp: str
    certificado: str
    nome_certificado: str


class ConfigArgsRobo(TypedDict):
    id_execucao: str
    sistema: str
    categoria: str
    credenciais: Credencial


class ArgumentosRobo(ConfigArgsRobo):
    nome_parte: str
    documento_parte: str
    credenciais: Credencial


__all__ = [
    "ArgumentosRobo",
    "AssuntoPJe",
    "AudienciaProcessoPJe",
    "BotData",
    "CapaPJe",
    "ConfigArgsRobo",
    "DataSave",
    "DictCredencial",
    "DictUsers",
    "DocumentoPJe",
    "ElawCondenacao",
    "ElawCustas",
    "ElawData",
    "ElawProvisionamento",
    "EsajCapa",
    "ExpedienteDocumentoPJe",
    "HealtCheck",
    "JusdsProvisionamento",
    "LoginForm",
    "Message",
    "MovimentacaoPJe",
    "PJeCapa",
    "PJeMovimentacao",
    "PartePJe",
    "PartesProjudiDict",
    "ProjudiCapa",
    "ProjudiMovimentacao",
    "RepresentantePJe",
    "RepresentantesProjudiDict",
]
