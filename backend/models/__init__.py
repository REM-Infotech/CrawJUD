"""Módulo de gestão de Models do banco de dados."""

from __future__ import annotations

import json
from pathlib import Path
from typing import TYPE_CHECKING, cast
from uuid import uuid4

from backend.extensions import db
from backend.models._bot import Bots, CredenciaisRobo, ExecucoesBot
from backend.models._users import LicenseUser, User
from backend.types_app.payloads import SystemBots

from ._jwt import TokenBlocklist

if TYPE_CHECKING:
    from flask import Flask
    from flask_keepass import KeepassManager
    from pykeepass import Group

    from backend.interfaces import DictCredencial, DictUsers
    from backend.types_app import Dict


__all__ = [
    "Bots",
    "CredenciaisRobo",
    "ExecucoesBot",
    "LicenseUser",
    "SystemBots",
    "TokenBlocklist",
    "User",
]


parent_path = Path(__file__).parent.resolve()


def init_database(app: Flask) -> None:
    """Inicializa o banco de dados."""
    with app.app_context(), db.session.no_autoflush:
        db.drop_all()
        db.create_all()

        user = (
            db.session.query(User).filter_by(login=app.config["ROOT_USERNAME"]).first()
        )

        if not user:
            root_user = User(
                login=app.config["ROOT_USERNAME"],
                email=app.config["ROOT_EMAIL"],
                nome_usuario=app.config.get("ROOT_DISPLAY_NAME", "Root User"),
            )
            root_user.senhacrip = app.config["ROOT_PASSWORD"]
            root_user.admin = True

            root_license = (
                db.session.query(LicenseUser)
                .filter(LicenseUser.Nome == "Root License")
                .first()
            )
            if not root_license:
                root_license = LicenseUser(
                    Nome="Root License",
                    descricao="Root License",
                )

            root_license.usuarios.append(root_user)
            db.session.add_all([root_license, root_user])
            db.session.commit()


def create_bots(app: Flask) -> None:
    with app.app_context():
        path_export = parent_path.joinpath("export.json")

        lic = (
            db.session.query(LicenseUser)
            .filter(LicenseUser.Nome == "Root License")
            .first()
        )

        with path_export.open("r", encoding="utf-8") as fp:
            list_data: list[Dict] = json.load(fp)

            list_bot_add = [
                Bots(**bot)
                for bot in list_data
                if not db.session.query(Bots).filter(Bots.Id == bot["Id"]).first()
            ]

            lic.bots.extend(list_bot_add)

            db.session.add_all(list_bot_add)
            db.session.commit()


def load_credentials(app: Flask) -> None:
    path_credentials = parent_path.joinpath("credentials.json")

    if path_credentials.exists():
        list_data: list[DictCredencial] = json.loads(path_credentials.read_text())
        with app.app_context():
            lic = (
                db.session.query(LicenseUser)
                .filter(LicenseUser.Nome == "Root License")
                .first()
            )

            keepass: KeepassManager = app.extensions["keepass"]

            sistemas = {}
            for item in list_data:
                sistemas[item["sistema"]] = sistemas.get(item["sistema"], 0) + 1

            list_cred_add: list[CredenciaisRobo] = []
            for sistema in sistemas:
                group = cast(
                    "Group",
                    keepass.find_groups(name=sistema.upper(), first=True),
                )
                if not group:
                    group = keepass.add_group(
                        destination_group=keepass.root_group,
                        group_name=sistema.upper(),
                    )

                filtered_list: list[DictCredencial] = list(
                    filter(lambda x: x["sistema"] == str(sistema), list_data),
                )
                for item in filtered_list:
                    entry = keepass.find_entries(
                        title=item["nome_credencial"],
                        first=True,
                    )

                    if not entry:
                        rastreio = str(uuid4())
                        entry = keepass.add_entry(
                            destination_group=group,
                            title=item["nome_credencial"],
                            username=item["login"],
                            password=item["password"],
                            tags=[item["login_metodo"]],
                            notes=rastreio,
                        )

                    rastreio = str(entry.notes)
                    if item.get("otp"):
                        entry.otp = item.get("otp")

                    if item.get("certificado"):
                        path_cert = Path(item.get("certificado"))
                        attachment_name = path_cert.name

                        if not keepass.find_attachments(filename=attachment_name):
                            attachment_data = path_cert.read_bytes()

                            binary_id = keepass.add_binary(attachment_data)
                            entry.add_attachment(
                                id=binary_id,
                                filename=attachment_name,
                            )

                    list_cred_add.append(
                        CredenciaisRobo(
                            nome_credencial=item["nome_credencial"],
                            sistema=sistema.upper(),
                            login_metodo=item["login_metodo"],
                            rastreio=rastreio,
                        ),
                    )

            lic.credenciais.extend(list_cred_add)
            db.session.add_all(list_cred_add)
            db.session.commit()

            keepass.save()


def import_users(app: Flask) -> None:
    path_users = parent_path.joinpath("users_202511251518.json")

    if path_users.exists():
        with app.app_context():
            text_users = path_users.read_text(encoding="utf-8")
            users: list[DictUsers] = json.loads(text_users)

            license_ = db.session.query(LicenseUser).first()
            list_users: list[User] = []

            for user in users:
                existing_user = (
                    db.session.query(User).filter(User.login == user["login"]).first()
                )

                if not existing_user:
                    new_user = User(
                        login=user["login"],
                        nome_usuario=user["nome_usuario"],
                        email=user["email"],
                        password=user["password"],
                    )

                    license_.usuarios.append(new_user)
                    list_users.append(new_user)

            db.session.add_all(list_users)
            db.session.commit()
