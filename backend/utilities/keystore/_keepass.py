from __future__ import annotations

from contextvars import ContextVar
from pathlib import Path
from typing import TYPE_CHECKING, TypedDict

from pykeepass import Entry, Group, PyKeePass

if TYPE_CHECKING:
    from uuid import UUID

    from flask import Flask

KWARGS: KeePassKwargs = {}

type AnyType = any


class KeePassKwargs(TypedDict, total=False):
    # title of entry to find
    title: str

    # username of entry to find
    username: str

    # password of entry to find
    password: str

    # url of entry to find
    url: str

    # notes of entry to find
    notes: str

    # otp string of entry to find
    otp: str

    # custom string fields.
    # (eg. {'custom_field1': 'custom value', 'custom_field2': 'custom value'})
    string: dict[str, str]

    # entry UUID
    uuid: UUID

    # entry tags
    tags: list[str]

    # autotype string is enabled
    autotype_enabled: bool

    # autotype string
    autotype_sequence: str

    # autotype target window filter string
    autotype_window: str

    # search under this group
    group: Group

    # return first match or None if no matches.
    # Otherwise return list of Entry matches. (default False)
    first: bool

    # include history entries in results. (default False)
    history: bool

    # search recursively
    recursive: bool

    # interpret search strings given above as XSLT style regexes
    regex: bool

    # regex search flags
    flags: str


class FlaskKeepass(PyKeePass):
    def __init__(
        self,
        app: Flask | None = None,
        filename: str | Path | None = None,
        password: str | Path | None = None,
        keyfile: str | None = None,
        transformed_key: str | None = None,
        *,
        decrypt: bool = True,
    ) -> None:

        self._filename = filename
        self._password = password
        self._keyfile = keyfile
        self._transformed_key = transformed_key
        self._decrypt = decrypt

        if app is not None:
            self.init_app(app, filename, password, keyfile, transformed_key, decrypt)

    def init_app(
        self,
        app: Flask,
        filename: str | Path | None = None,
        password: str | None = None,
        keyfile: str | Path | None = None,
        transformed_key: str | None = None,
        *,
        decrypt: bool = True,
    ) -> None:

        filename = app.config.get("KEEPASS_FILENAME", filename or self._filename)
        password = app.config.get("KEEPASS_PASSWORD", password or self._password)
        keyfile = app.config.get("KEEPASS_KEYFILE", keyfile or self._keyfile)
        transformed_key = app.config.get(
            "KEEPASS_TRANSFORMED_KEY",
            transformed_key or self._transformed_key,
        )
        decrypt = app.config.get("KEEPASS_DECRYPT", decrypt or self._decrypt)

        if isinstance(decrypt, str):
            decrypt = decrypt is None or decrypt in [True, "True", "true", "1", 1]

        if isinstance(filename, Path):
            filename = str(filename)

        if isinstance(keyfile, Path):
            keyfile = str(keyfile)

        super().__init__(filename, password, keyfile, transformed_key, decrypt)

        if hasattr(app, "extensions") and not app.extensions.get("keepass"):
            app.extensions["keepass"] = self

    def find_entries(
        self,
        *,
        recursive: bool = True,
        path: str | None = None,
        group: str | None = None,
        kwargs: KeePassKwargs = KWARGS,
    ) -> Entry | list[Entry] | None:
        return super().find_entries(recursive, path, group, **kwargs)


_ctx_current_db = ContextVar(
    "current_keepass_db",
    default=None,
    type=FlaskKeepass | None,
)


def get_current_keepass_db() -> FlaskKeepass | None:
    """Recupere a instância atual do KeePass do contexto.

    Returns:
        FlaskKeepass | None: Instância atual do KeePass ou None se não existir.

    """
    return _ctx_current_db.get()
