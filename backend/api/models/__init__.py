"""Módulo de gestão de Models do banco de dados."""

from __future__ import annotations

import json
from pathlib import Path
from typing import TYPE_CHECKING, TypedDict

from backend.api.extensions import db
from backend.api.models._bot import Bots, CredenciaisRobo, ExecucoesBot
from backend.api.models._users import LicenseUser, User

from ._jwt import TokenBlocklist

if TYPE_CHECKING:
    from flask import Flask

    from backend.types_app import Dict

__all__ = [
    "Bots",
    "CredenciaisRobo",
    "ExecucoesBot",
    "LicenseUser",
    "TokenBlocklist",
    "User",
]


class DictUsers(TypedDict):
    id: int
    login: str
    nome_usuario: str
    email: str
    password: str
    login_time: str
    verification_code: str
    login_id: str
    filename: str
    blob_doc: bytes
    licenseus_id: int


def init_database(app: Flask) -> None:
    """Inicializa o banco de dados."""
    with app.app_context(), db.session.no_autoflush:
        db.drop_all()
        db.create_all()

        user = (
            db.session.query(User)
            .filter_by(login=app.config["ROOT_USERNAME"])
            .first()
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
        path_export = Path(__file__).parent.joinpath("export.json")

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
                if not db.session.query(Bots)
                .filter(Bots.Id == bot["Id"])
                .first()
            ]

            lic.bots.extend(list_bot_add)

            db.session.add_all(list_bot_add)
            db.session.commit()


def load_credentials(app: Flask) -> None:
    path_credentials = Path(__file__).parent.joinpath(
        "credentials.json",
    )

    if path_credentials.exists():
        with (
            app.app_context(),
            path_credentials.open("r", encoding="utf-8") as fp,
        ):
            lic = (
                db.session.query(LicenseUser)
                .filter(LicenseUser.Nome == "Root License")
                .first()
            )
            list_data: list[Dict] = json.load(fp)

            list_cred_add = [
                CredenciaisRobo(**cred)
                for cred in list_data
                if not db.session.query(CredenciaisRobo)
                .filter(CredenciaisRobo.Id == cred["Id"])
                .first()
            ]

            lic.credenciais.extend(list_cred_add)
            db.session.add_all(list_cred_add)
            db.session.commit()


def import_users(app: Flask) -> None:
    path_users = Path(__file__).parent.joinpath(
        "users_202511251518.json",
    )

    if path_users.exists():
        users: list[DictUsers] = json.loads(
            path_users.read_text(encoding="utf-8"),
        )["users"]

        with app.app_context():
            license_ = db.session.query(LicenseUser).first()
            list_users: list[User] = []
            for user in users:
                existing_user = (
                    db.session.query(User)
                    .filter(User.login == user["login"])
                    .first()
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
