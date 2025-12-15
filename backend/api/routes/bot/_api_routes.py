"""Forneça rotas para bots, credenciais e execução de robôs."""

from __future__ import annotations

import traceback
from base64 import b64encode
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
    jwt_required,
)

from backend.api._forms.head import FormBot
from backend.api.constants import SISTEMAS
from backend.api.decorators import CrossDomain
from backend.api.resources import gerar_id

if TYPE_CHECKING:
    from backend.api.extensions._minio import Minio
    from backend.types_app import Sistemas
    from backend.types_app.responses import (
        PayloadDownloadExecucao,
        Response,
    )

bots = Blueprint("bots", __name__, url_prefix="/bot")


def is_sistema(valor: Sistemas) -> bool:
    """Verifique se o valor informado pertence aos sistemas cadastrados.

    Args:
        valor (Sistemas): Valor a ser verificado.

    Returns:
        bool: Indica se o valor está em SISTEMAS.

    """
    return valor in SISTEMAS


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

        except Exception as e:  # noqa: BLE001
            _exc = "\n".join(traceback.format_exception(e))

    return make_response(jsonify(payload), code)


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
