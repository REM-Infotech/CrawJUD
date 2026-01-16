"""Forneça rotas para bots, credenciais e execução de robôs."""

from __future__ import annotations

import traceback
from base64 import b64encode
from pathlib import Path
from tempfile import gettempdir
from typing import TYPE_CHECKING, TypedDict
from uuid import uuid4

from flask_jwt_extended import get_current_user
from quart import current_app, jsonify
from quart.wrappers import Response

from backend.api._forms.head import FormBot
from backend.api.decorators import CrossDomain, async_jwt_required
from backend.api.resources import gerar_id
from backend.api.routes._blueprints import bots

if TYPE_CHECKING:
    from backend.extensions._minio import Minio
    from backend.models import User
    from typings import (
        PayloadDownloadExecucao,
        Response,
        Sistemas,
    )

SISTEMAS: set[Sistemas] = {
    "projudi",
    "elaw",
    "esaj",
    "pje",
    "jusds",
    "csi",
}


def is_sistema(valor: Sistemas) -> bool:
    """Verifique se o valor informado pertence aos sistemas cadastrados.

    Args:
        valor (Sistemas): Valor a ser verificado.

    Returns:
        bool: Indica se o valor está em SISTEMAS.

    """
    return valor in SISTEMAS


class CredenciaisSelect(TypedDict):  # noqa: D101
    value: int
    text: str


@bots.post("/<string:sistema>/run")
@CrossDomain(origin="*", methods=["get", "post", "options"])
@async_jwt_required
async def run_bot(sistema: Sistemas) -> Response:
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
            form = await FormBot.load_form()
            pid_exec = gerar_id()
            form.handle_task(pid_exec=pid_exec)

            payload = {
                "title": "Sucesso",
                "message": "Robô inicializado com sucesso!",
                "status": "success",
                "id_execucao": pid_exec,
                "pid_resumido": pid_exec,
            }
            code = 200

        except Exception as e:  # noqa: BLE001
            _exc = "\n".join(traceback.format_exception(e))

    response = jsonify(payload)
    response.status_code = code
    return response


@bots.get("/execucoes/<string:id_execucao>/download")
@CrossDomain(origin="*", methods=["get", "post", "options"])
@async_jwt_required
def download_execucao(id_execucao: str) -> Response[PayloadDownloadExecucao]:
    """Baixe o arquivo de execução do bot pelo PID informado.

    Args:
        id_execucao (str): Identificador da execução do bot.

    Returns:
        Response[PayloadDownloadExecucao]: Resposta com arquivo codificado.

    """
    storage: Minio = current_app.extensions["storage"]

    temp_dir = Path(gettempdir()).joinpath(f"crawjud-{uuid4().hex}")

    if not temp_dir.exists():
        temp_dir.mkdir(parents=True, exist_ok=True)

    file_path = temp_dir.joinpath(f"{id_execucao}.zip")
    if file_path.exists():
        file_path.unlink()

    storage.fget_object(
        bucket_name="outputexec-bots",
        object_name=f"{id_execucao}.zip",
        file_path=str(file_path),
    )

    with file_path.open("rb") as file:
        file_data = file.read()

    payload = jsonify({
        "content": b64encode(file_data).decode("utf-8"),
        "file_name": f"{id_execucao}.zip",
    })
    payload.status_code = 200
    return payload


@bots.get("/listagem")
@async_jwt_required
def listagem() -> Response:  # noqa: D103

    user: User = get_current_user()

    return jsonify({
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
    })


@async_jwt_required
@bots.get("/listagem-credenciais/<string:sistema>")
async def on_provide_credentials(sistema: Sistemas) -> Response:  # noqa: RUF029
    """Lista as credenciais disponíveis para o sistema informado."""
    list_credentials = [CredenciaisSelect(value=None, text="Selecione")]
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

    return jsonify(list_credentials)
