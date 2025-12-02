from __future__ import annotations

import re
from contextlib import suppress
from typing import TYPE_CHECKING
from uuid import uuid4

import bcrypt
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped  # noqa: TC002

from backend.api import crypt_context
from backend.api.extensions import db

if TYPE_CHECKING:
    from backend.api.models._bot import Bots, CredenciaisRobo, ExecucoesBot

rel = db.relationship
salt = bcrypt.gensalt()


def _generate_key() -> str:
    return re.sub(
        r"(.{8})(.{8})(.{8})(.{8})",
        r"\1-\2-\3-\4",
        uuid4().hex,
    ).upper()


class LicenseUser(db.Model):
    __tablename__ = "licencas"
    Id: int = Column("id", Integer, primary_key=True, nullable=False)
    ProductKey: str = Column(
        "product_key",
        String(35),
        default=_generate_key,
    )
    descricao: int = Column(
        "descricao",
        String(length=256),
        nullable=False,
    )
    Nome: str = Column("nome", String(64))

    CPF: str = Column(
        "cpf",
        String(14),
        nullable=False,
        default="000.000.000-00",
    )
    CNPJ: str = Column(
        "cnpj",
        String(18),
        nullable=False,
        default="00.000.000/0000-00",
    )

    bots: Mapped[list[Bots]] = rel(back_populates="license_")
    usuarios: Mapped[list[User]] = rel(back_populates="license_")
    credenciais: Mapped[list[CredenciaisRobo]] = rel(
        back_populates="license_",
    )


class User(db.Model):
    __tablename__ = "usuarios"
    Id: int = Column("id", Integer, primary_key=True)
    login: str = Column(
        "username",
        String(length=30),
        nullable=False,
        unique=True,
    )
    nome_usuario: str = Column(
        "display_name",
        String(length=64),
        nullable=False,
    )
    email: str = Column(
        "email",
        String(length=50),
        nullable=False,
        unique=True,
    )
    password: str = Column(
        "password",
        String(length=128),
        nullable=False,
    )
    admin: bool = Column("admin", Boolean, default=False)

    execucoes: Mapped[list[ExecucoesBot]] = rel(
        back_populates="usuario",
    )

    license_id: int = Column(Integer, ForeignKey("licencas.id"))
    license_: Mapped[LicenseUser] = rel(back_populates="usuarios")

    @classmethod
    def authenticate(cls, username: str, password: str) -> bool:
        user = db.session.query(cls).filter(cls.login == username).first()
        return user is not None and user.check_password(password)

    @property
    def senhacrip(self) -> str:
        return self.senhacrip

    @senhacrip.setter
    def senhacrip(self, senha_texto: str) -> None:
        self.password = crypt_context.hash(senha_texto, scheme="argon2")

    def check_password(self, senha_texto_claro: str) -> bool:
        needs_update = False
        valid_hash = False
        with suppress(Exception):
            valid_hash = crypt_context.verify(
                senha_texto_claro,
                self.password,
                scheme="argon2",
            )

        if not valid_hash:
            with suppress(Exception):
                valid_hash = bcrypt.checkpw(
                    senha_texto_claro.encode("utf-8"),
                    self.password.encode("utf-8"),
                )
                needs_update = True

        if valid_hash:
            if needs_update:
                self.password = crypt_context.hash(
                    senha_texto_claro,
                    scheme="argon2",
                )
                db.session.add(self)
                db.session.commit()

            return True

        return False
