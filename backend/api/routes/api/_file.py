from base64 import b64decode
from typing import TypedDict

from quart import abort, request

from backend.api.decorators import async_jwt_required
from backend.api.routes._blueprints import upload


class DataFileUpload(TypedDict):
    """Defina os campos necessários para upload de arquivo.

    name: Nome do arquivo.
    fileSize: Tamanho do arquivo em bytes.
    chunk: Dados do arquivo em bytes.
    """

    name: str
    fileSize: int
    chunk: str
    seed: str


@upload.put("/")
@async_jwt_required
def upload_arquivo() -> None:

    try:
        request_data: DataFileUpload = request.get_json()
        _chunk_bytes = b64decode(request_data["chunk"])

    except Exception:  # noqa: BLE001
        abort(500)
