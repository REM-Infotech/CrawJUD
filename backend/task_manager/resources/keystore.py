"""Keepass wrapper."""

from __future__ import annotations

from os import environ as env
from typing import TYPE_CHECKING, TypedDict

from pykeepass import Entry, PyKeePass

if TYPE_CHECKING:
    import uuid as pyuuid

    from pykeepass.group import Group


class KeePassFindEntryKwargs(TypedDict):
    """Defina os argumentos aceitos para busca de entradas no KeePass.

    Args:
        path (list[str]): Caminho dos grupos.
        title (str): Título da entrada.
        username (str): Nome de usuário.
        password (str): Senha.
        url (str): URL associada.
        notes (str): Notas da entrada.
        otp (str): Código OTP.
        string (dict[str, str]): Campos personalizados.
        uuid (pyuuid.UUID): UUID da entrada.
        tags (list[str]): Lista de tags.
        autotype_enabled (bool): Autotype habilitado.
        autotype_sequence (str): Sequência de autotype.
        autotype_window (str): Janela de autotype.
        group (Group): Grupo da entrada.
        first (bool): Retorne apenas o primeiro resultado.
        history (bool): Inclua histórico.
        recursive (bool): Busca recursiva.
        regex (bool): Use regex na busca.
        flags (str): Flags adicionais.

    """

    path: list[str]
    title: str
    username: str
    password: str
    url: str
    notes: str
    otp: str
    string: dict[str, str]
    uuid: pyuuid.UUID
    tags: list[str]
    autotype_enabled: bool
    autotype_sequence: str
    autotype_window: str
    group: Group
    first: bool
    history: bool
    recursive: bool
    regex: bool
    flags: str


class KeyStore(PyKeePass):
    """Implemente um wrapper para interagir com um banco KeePass via PyKeePass.

    Esta classe permite inicializar e buscar entradas em um banco KeePass.
    """

    def __init__(
        self,
        arquivo_kbdx: str | None = None,
        senha_kbdx: str | None = None,
    ) -> None:
        """Inicialize o KeyStore com o arquivo e senha do banco KeePass.

        Args:
            arquivo_kbdx (str | None): Caminho do arquivo KeePass.
            senha_kbdx (str | None): Senha do arquivo KeePass.

        """
        if not arquivo_kbdx:
            arquivo_kbdx = env.get("KBDX_PATH")

        if not senha_kbdx:
            senha_kbdx = env.get("KBDX_PASSWORD")

        super().__init__(filename=arquivo_kbdx, password=senha_kbdx)

    def find_entries(
        self,
        kwargs: KeePassFindEntryKwargs,
        *,
        recursive: bool = True,
        path: str | None = None,
        group: Group = None,
    ) -> Entry | list[Entry] | None:
        """Busque entradas no banco KeePass conforme os critérios informados.

        Args:
            kwargs (KeePassFindEntryKwargs): Critérios de busca.
            recursive (bool): Busca recursiva nos grupos.
            path (str | None): Caminho do grupo.
            group (Group | None): Grupo KeePass.

        Returns:
            (Entry | list[Entry] | None): Entradas encontradas ou None.

        """
        return super().find_entries(recursive, path, group, **kwargs)
