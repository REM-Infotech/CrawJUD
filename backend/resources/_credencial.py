from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Literal, TypedDict, Unpack, cast
from uuid import uuid4

from flask import current_app
from flask_jwt_extended import get_current_user
from werkzeug.datastructures import FileStorage

from backend.models import CredenciaisRobo, LicenseUser, User

if TYPE_CHECKING:
    from flask import Flask
    from flask_keepass import KeepassManager
    from flask_sqlalchemy import SQLAlchemy
    from pykeepass.group import Group

    from backend.types_app import Sistemas

type LoginMetodoSimplificado = Literal["pw", "cert"]


class CredencialBotDict(TypedDict):
    nome_credencial: str
    sistema: Sistemas
    login_metodo: LoginMetodoSimplificado
    login: str | None
    password: str | None
    certificado: FileStorage | None
    cpf_cnpj_certificado: str | None
    senha_certificado: str | None
    otp: str | None
    requer_duplo_fator: bool


class CredencialBot:
    nome_credencial: str
    sistema: Sistemas
    login_metodo: LoginMetodoSimplificado
    login: str | None
    password: str | None
    certificado: FileStorage | None
    cpf_cnpj_certificado: str | None
    senha_certificado: str | None
    otp: str | None
    requer_duplo_fator: bool

    def __init__(self, app: Flask, **kwargs: Unpack[CredencialBotDict]) -> None:

        self.keepass: KeepassManager = app.extensions["keepass"]

        cred_empty = CredencialBotDict(
            nome_credencial="",
            sistema="",
            login_metodo="",
            login="",
            password="",
            certificado="",
            cpf_cnpj_certificado="",
            senha_certificado="",
            otp="",
            requer_duplo_fator=False,
        )

        for item in list(cred_empty.keys()):
            setattr(self, item, kwargs.get(item, cred_empty.get(item)))

    def cadastro(self) -> None:

        keepass = self.keepass
        sistema = self.sistema

        group = cast(
            "Group",
            keepass.find_groups(name=sistema.upper(), first=True),
        )
        if not group:
            group = keepass.add_group(
                destination_group=keepass.root_group,
                group_name=sistema.upper(),
            )

        entry = keepass.find_entries(
            title=self.nome_credencial,
            first=True,
        )

        if entry:
            rastreio = getattr(entry, "notes", None)
        elif not entry:
            rastreio = str(uuid4())
            entry = keepass.add_entry(
                destination_group=group,
                title=self.nome_credencial,
                username=self.login,
                password=self.password,
                tags=self.login_metodo,
                notes=rastreio,
            )

        if self.otp:
            entry.otp = self.otp

        if self.certificado:
            if isinstance(self.certificado, FileStorage):
                path_temp = Path.cwd().joinpath("temp")
                path_temp.mkdir(exist_ok=True, parents=True)
                self.certificado.save(str(path_temp))

                self.certificado = str(path_temp)

            path_cert = Path(self.certificado)
            attachment_name = path_cert.name

            if not keepass.find_attachments(filename=attachment_name):
                attachment_data = path_cert.read_bytes()

                binary_id = keepass.add_binary(attachment_data)
                entry.add_attachment(
                    id=binary_id,
                    filename=attachment_name,
                )

        db: SQLAlchemy = current_app.extensions["sqlalchemy"]

        cred = CredenciaisRobo(
            nome_credencial=self.nome_credencial,
            sistema=sistema.upper(),
            login_metodo=self.login_metodo,
            rastreio=rastreio,
        )

        user: User = get_current_user()

        license_ = (
            db.session.query(LicenseUser)
            .filter(LicenseUser.ProductKey == user.license_.ProductKey)
            .first()
        )

        license_.credenciais.append(cred)

        db.session.add(cred)
        db.session.commit()

        return
