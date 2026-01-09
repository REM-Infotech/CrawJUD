"""Configuraçõs gerais do CrawJUD."""

from pathlib import Path

from dynaconf import Dynaconf

from ._interfaces import CeleryConfig

WORKDIR = Path(__file__).parent.resolve()

setting_file = str(WORKDIR.joinpath("settings.yaml"))
secrets_file = str(WORKDIR.joinpath(".secrets.yaml"))

settings = Dynaconf(
    lowercase_read=False,
    envvar_prefix="CRAWJUD",
    settings_files=[setting_file, secrets_file],
    environments=True,
    load_dotenv=True,
    commentjson_enabled=True,
    merge_enabled=True,
    dotenv_override=True,
)


__all__ = ["CeleryConfig", "settings"]
