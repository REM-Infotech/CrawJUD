"""Configuraçõs gerais do CrawJUD."""

import logging
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

ACCESS_FMT = '%(levelprefix)s %(client_addr)s - "%(request_line)s" %(status_code)s'
LOG_LEVEL = logging.DEBUG

name = "crawjud-api.log"
PATH_LOG = Path.cwd().joinpath("logs", name)
if not PATH_LOG.parent.exists():
    PATH_LOG.parent.mkdir(exist_ok=True)
    PATH_LOG.touch()

LOG_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": "%(levelprefix)s %(asctime)s %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "access": {
            "()": "uvicorn.logging.AccessFormatter",
            "fmt": ACCESS_FMT,
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
        "access": {
            "formatter": "access",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
        "file_log": {
            "formatter": "default",
            "class": "logging.FileHandler",
            "filename": str(PATH_LOG),
        },
    },
    "loggers": {
        "uvicorn": {"handlers": ["default"], "level": LOG_LEVEL},
        "uvicorn.error": {
            "handlers": ["default", "file_log"],
            "level": LOG_LEVEL,
            "propagate": False,
        },
        "uvicorn.access": {
            "handlers": ["access", "file_log"],
            "level": LOG_LEVEL,
            "propagate": False,
        },
        "uvicorn.asgi": {
            "handlers": ["default", "file_log"],
            "level": LOG_LEVEL,
            "propagate": False,
        },
        "uvicorn.lifespan": {
            "handlers": ["default", "file_log"],
            "level": LOG_LEVEL,
            "propagate": False,
        },
    },
}


__all__ = ["CeleryConfig", "settings"]
