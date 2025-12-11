"""Forneça rotas para bots, credenciais e execução de robôs."""

from __future__ import annotations

import traceback
from base64 import b64encode
from datetime import datetime
from pathlib import Path
from tempfile import gettempdir
from typing import TYPE_CHECKING
from uuid import uuid4

from flask import (
    Blueprint,
    current_app,
    jsonify,
    make_response,
)
from flask.wrappers import Response
from flask_jwt_extended import (
    get_current_user,
    jwt_required,
)

from backend.api._forms.head import FormBot
from backend.api.constants import SISTEMAS
from backend.api.decorators import CrossDomain
from backend.api.resources import gerar_id

if TYPE_CHECKING:
    from backend.api.extensions._minio import Minio
    from backend.api.models import User
    from backend.api.types_app import Sistemas
    from backend.task_manager.types_app.responses import (
        PayloadDownloadExecucao,
        Response,
    )

bots = Blueprint("bots", __name__, url_prefix="/bot")


def format_time(val: datetime | None) -> str | None:
    """Formata data/hora para string legível ou retorne valor original."""
    if val and isinstance(val, datetime):
        return val.strftime("%d/%m/%Y, %H:%M:%S")

    return val


def is_sistema(valor: Sistemas) -> bool:
    """Verifique se o valor informado pertence aos sistemas cadastrados.

    Args:
        valor (Sistemas): Valor a ser verificado.

    Returns:
        bool: Indica se o valor está em SISTEMAS.

    """
    return valor in SISTEMAS


@bots.route("/listagem")
@jwt_required()
def listagem() -> Response:
    """Lista todos os bots disponíveis para o usuário autenticado.

    Returns:
        Response: Resposta HTTP com a listagem dos bots.

    """
    user: User = get_current_user()

    return make_response(
        jsonify({
            "listagem": [
                {
                    "Id": bot.Id,
                    "display_name": bot.display_name,
                    "sistema": bot.sistema,
                    "categoria": bot.categoria,
                    "configuracao_form": bot.configuracao_form,
                    "descricao": bot.descricao,
                }
                for bot in user.license_.bots
            ],
        }),
        200,
    )


@bots.get("/<string:sistema>/credenciais")
@jwt_required()
def provide_credentials(sistema: Sistemas) -> Response:
    """Lista as credenciais disponíveis para o sistema informado.

    Args:
        sistema (Sistemas): Sistema para filtrar as credenciais.

    Returns:
        Response: Resposta HTTP com as credenciais filtradas.

    """
    list_credentials = []
    if is_sistema(sistema):
        system = sistema.upper()
        user: User = get_current_user()

        lic = user.license_

        list_credentials.extend([
            {"value": credential.Id, "text": credential.nome_credencial}
            for credential in list(
                filter(
                    lambda credential: credential.sistema == system,
                    lic.credenciais,
                ),
            )
        ])

    return make_response(
        jsonify({"credenciais": list_credentials}),
        200,
    )


@bots.post("/<string:sistema>/run")
@CrossDomain(origin="*", methods=["get", "post", "options"])
@jwt_required()
def run_bot(sistema: Sistemas) -> Response:
    """Inicie a execução de um robô para o sistema informado.

    Args:
        sistema (Sistemas): Sistema para executar o robô.

    Returns:
        Response: Resposta HTTP com o status da execução.

    """
    payload = {
        "title": "Erro",
        "message": "Erro ao iniciar robô",
        "status": "error",
    }

    if is_sistema(sistema):
        code = 500
        try:
            form = FormBot.load_form()
            pid_exec = gerar_id()
            form.handle_task(pid_exec=pid_exec)

            payload = {
                "title": "Sucesso",
                "message": "Robô inicializado com sucesso!",
                "status": "success",
                "pid": pid_exec,
                "pid_resumido": pid_exec,
            }
            code = 200

        except Exception as e:
            _exc = "\n".join(traceback.format_exception(e))

    return make_response(jsonify(payload), code)


@bots.get("/execucoes")
@jwt_required()
def execucoes() -> Response:
    """Lista execuções dos bots do usuário autenticado.

    Returns:
        Response: Resposta HTTP com execuções dos bots.

    """
    # Obtém o usuário autenticado
    user: User = get_current_user()

    # Recupera execuções dos bots do usuário
    execucao = user.execucoes

    # Define payload padrão caso não haja execuções
    payload = jsonify([
        {
            "id": 0,
            "bot": "vazio",
            "pid": "vazio",
            "status": "vazio",
            "data_inicio": "vazio",
            "data_fim": "vazio",
        },
    ])
    if execucao:
        # Retorna lista de execuções se houver
        payload = jsonify([
            {
                "id": item.Id,
                "bot": item.bot.display_name,
                "pid": item.pid,
                "status": item.status,
                "data_inicio": format_time(item.data_inicio),
                "data_fim": format_time(item.data_fim),
            }
            for item in execucao
        ])

    return make_response(payload, 200)


@bots.get("/execucoes/<string:pid>/download")
@jwt_required()
def download_execucao(pid: str) -> Response[PayloadDownloadExecucao]:
    """Baixe o arquivo de execução do bot pelo PID informado.

    Args:
        pid (str): Identificador da execução do bot.

    Returns:
        Response[PayloadDownloadExecucao]: Resposta com arquivo codificado.

    """
    storage: Minio = current_app.extensions["storage"]

    temp_dir = Path(gettempdir()).joinpath(f"crawjud-{uuid4().hex}")

    if not temp_dir.exists():
        temp_dir.mkdir(parents=True, exist_ok=True)

    file_path = temp_dir.joinpath(f"{pid}.zip")
    if file_path.exists():
        file_path.unlink()

    storage.fget_object(
        bucket_name="outputexec-bots",
        object_name=f"{pid}.zip",
        file_path=str(file_path),
    )

    with file_path.open("rb") as file:
        file_data = file.read()

    payload = jsonify({
        "content": b64encode(file_data).decode("utf-8"),
        "file_name": f"{pid}.zip",
    })

    return make_response(payload, 200)
