"""Gerenciador de arquivos recebidos para a execução do robô."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING
from zipfile import ZIP_DEFLATED, ZipFile

from dotenv import load_dotenv
from minio import Minio as MinioClient
from tqdm import tqdm

from backend.config import settings
from backend.resources.formatadores import formata_string

if TYPE_CHECKING:
    from celery import Celery
    from minio.datatypes import Object

    from backend.controllers.head import CrawJUD

WORKDIR = Path.cwd()
load_dotenv()


class FileManager(MinioClient):
    """Gerenciador de arquivos recebidos para a execução do robô."""

    celery: Celery

    def __init__(self, bot: CrawJUD) -> None:
        """Inicialize o gerenciador com o bot informado.

        Args:
            bot (CrawJUD): Instância do robô principal.

        """
        dict_config = dict(list(settings.as_dict().items()))
        super().__init__(
            endpoint=dict_config["MINIO_ENDPOINT"],
            access_key=dict_config.get("MINIO_ACCESS_KEY"),
            secret_key=dict_config.get("MINIO_SECRET_KEY"),
            session_token=dict_config.get("MINIO_SESSION_TOKEN"),
            secure=dict_config.get("MINIO_SECURE", False),
            region=dict_config.get("MINIO_REGION"),
            http_client=dict_config.get("MINIO_HTTP_CLIENT"),
            credentials=dict_config.get("MINIO_CREDENTIALS"),
            cert_check=dict_config.get("MINIO_CERT_CHECK", False),
        )

        self.bot = bot

    def __filter_files(self, item: Object) -> bool:
        file_name = formata_string(Path(item.object_name).name)

        is_arquivo = False
        for arquivo in self.lista_arquivos:
            if arquivo == file_name:
                is_arquivo = True
                break

        return is_arquivo

    def download_files(self) -> None:
        """Baixe arquivos do Minio para o diretório de saída do robô."""
        if self.bot.config.get("folder_objeto_minio"):
            self.lista_arquivos = [self.bot.xlsx]
            if self.bot.anexos:
                self.lista_arquivos.extend(self.bot.anexos)

            folder_prefix = str(self.bot.config["folder_objeto_minio"])

            files_bucket = list(
                self.list_objects(
                    "outputexec-bots",
                    prefix=folder_prefix,
                    recursive=True,
                ),
            )
            message = "Baixando arquivos"
            message_type = "log"
            self.bot.print_message(message=message, message_type=message_type)
            for item in tqdm(files_bucket):
                file_name = Path(item.object_name).name
                file_path = self.bot.output_dir_path.joinpath(file_name)

                if not file_path.exists():
                    _obj = self.fget_object(
                        item.bucket_name,
                        item.object_name,
                        str(file_path),
                    )

                    message = f'Arquivo "{file_name}" baixado com sucesso!'
                    self.bot.print_message(
                        message=message,
                        message_type="success",
                    )

    def upload_file(self) -> str:
        """Gere e envie arquivo zip ao Minio, retornando URL.

        Returns:
            str: URL para download do arquivo zip enviado.

        """
        zipfile = self.__zip_result()

        self.fput_object("outputexec-bots", zipfile.name, str(zipfile))

        return self.get_presigned_url(
            "GET",
            "outputexec-bots",
            object_name=zipfile.name,
        )

    def __zip_result(self) -> Path:
        zip_filename = f"{self.bot.pid}.zip"
        source_dir = self.bot.output_dir_path
        output_dir = WORKDIR.joinpath("archives", zip_filename)

        output_dir.parent.mkdir(exist_ok=True, parents=True)

        with ZipFile(output_dir, "w", ZIP_DEFLATED) as zipfile:
            for root, _, files in source_dir.walk():
                for file in files:
                    if self.bot.pid in file and ".log" not in file:
                        file_path = root.joinpath(file)
                        arcname = file_path.relative_to(source_dir)
                        zipfile.write(file_path, arcname)

        return output_dir
