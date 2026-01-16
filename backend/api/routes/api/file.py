# ruff: noqa: D103, D100
from asyncio import create_task
from base64 import b64decode
from typing import TypedDict

from quart import abort, request

from backend.api.decorators import async_jwt_required
from backend.api.routes._blueprints import upload
from backend.api.routes.web.file_upload.file_upload import uploader


class FileUploadArguments(TypedDict):
    name: str
    chunk: bytes
    current_size: int
    fileSize: int
    fileType: str
    seed: str


fileupload = set()


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
async def upload_arquivo() -> None:

    try:
        print("teste!")
        data = await request.get_json()
        data["content"] = b64decode(data["chunk"])

        fileupload.add(create_task(uploader(data)).add_done_callback(fileupload.discard))
        print(data["name"])

    except Exception:  # noqa: BLE001
        abort(500)
