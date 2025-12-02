"""Configurações celery."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from dynaconf import Dynaconf

if TYPE_CHECKING:
    from dynaconf.contrib import DynaconfConfig

PARENT_PATH = Path(__file__).parent.resolve()

setting_file = str(PARENT_PATH.joinpath("settings.yaml"))
secrets_file = str(PARENT_PATH.joinpath(".secrets.celery.yaml"))

config = Dynaconf(
    lowercase_read=False,
    envvar_prefix="CRAWJUD",
    settings_files=[setting_file, secrets_file],
    environments=True,
    load_dotenv=True,
    commentjson_enabled=True,
    merge_enabled=True,
    dotenv_override=True,
)


class CeleryConfig:
    """Configure variáveis do celery dinamicamente."""

    def __init__(self, values: DynaconfConfig) -> None:
        """Inicialize a configuração do celery com valores dinâmicos.

        Args:
            values (DynaconfConfig): Configurações dinâmicas.

        """
        for k, v in list(values.items()):
            if str(k).isupper():
                setattr(self, k.lower(), v)
