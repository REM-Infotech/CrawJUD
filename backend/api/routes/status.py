"""Rotas de status da API."""

from __future__ import annotations

from typing import TYPE_CHECKING

from quart import (
    Response,
    jsonify,
    redirect,
    request,
    send_from_directory,
    url_for,
)

from backend.api.decorators import async_jwt_required
from backend.extensions import app, db

if TYPE_CHECKING:
    from backend.dicionarios import HealtCheck

__all__ = ["app"]


@app.route("/health")
def health_check() -> HealtCheck:
    try:
        # Testa conexão com banco de dados
        db.session.execute(db.text("SELECT 1"))
        db_status = "ok"
        code_err = 200
    except Exception as e:  # noqa: BLE001
        app.logger.exception(f"Health check failed: {e}")
        db_status = "erro"
        code_err = 500

    resp = jsonify({
        "status": "ok" if db_status == "ok" else "erro",
        "database": db_status,
        "timestamp": str(db.func.now()),
    })

    resp.status_code = code_err

    return resp


@app.route("/", methods=["GET"])
def index() -> Response:
    return redirect(url_for("health_check"))


@app.route("/robots.txt")
async def static_from_root() -> Response:
    return await send_from_directory(app.static_folder, request.path[1:])


@app.route("/sessao-valida", methods=["GET"])
@async_jwt_required
def sessao_valida() -> Response:
    """Verifica se a sessão JWT é válida.

    Retorna um status 200 se a sessão for válida, caso contrário,
    retorna um erro 401.

    Returns:
        Response: Resposta HTTP indicando o status da sessão.

    """
    resp = jsonify({"msg": "Sessão válida"})
    resp.status_code = 200

    return resp
