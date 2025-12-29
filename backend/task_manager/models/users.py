"""Defina modelos de usuário e licença para autenticação e controle.

Este módulo contém:
- LicenseUser: modelo de licença de produto.
- User: modelo de usuário com autenticação e senha.
"""

from __future__ import annotations

import re
from typing import TYPE_CHECKING
from uuid import uuid4

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped  # noqa: TC002

from backend.extensions import crypt_context, db

if TYPE_CHECKING:
    from backend.task_manager.models.bot import ExecucoesBot

    from .bot import Bots, CredenciaisRobo

rel = db.relationship


def _generate_key() -> str:
    return re.sub(
        r"(.{8})(.{8})(.{8})(.{8})",
        r"\1-\2-\3-\4",
        uuid4().hex,
    ).upper()


class LicenseUser(db.Model):
    """Defina modelo de licença de produto para autenticação.

    Args:
        Nenhum.

    """

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
    """Represente usuário com autenticação e permissões.

    Atributos:
        Id (int): Identificador do usuário.
        login (str): Nome de usuário para login.
        nome_usuario (str): Nome de exibição do usuário.
        email (str): E-mail do usuário.
        password (str): Senha criptografada.
        admin (bool): Indica se é administrador.
        execucoes (list[ExecucoesBot]): Execuções do usuário.
        license_id (int): ID da licença associada.
        license_ (LicenseUser): Licença vinculada ao usuário.

    """

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
        """Autentique usuário verificando login e senha fornecidos.

        Args:
            username (str): Nome de usuário.
            password (str): Senha do usuário.

        Returns:
            bool: True se autenticado, False caso contrário.

        """
        user = db.session.query(cls).filter(cls.login == username).first()
        return user is not None and user.check_password(password)

    @property
    def senhacrip(self) -> str:
        """Retorne a senha criptografada do usuário."""
        return self.senhacrip

    @senhacrip.setter
    def senhacrip(self, senha_texto: str) -> None:
        self.password = crypt_context.hash(senha_texto)

    def check_password(self, senha_texto_claro: str) -> bool:
        """Verifique se a senha fornecida corresponde à senha salva.

        Args:
            senha_texto_claro (str): Senha em texto claro.

        Returns:
            bool: True se a senha for válida, False caso contrário.

        """
        valid_hash = crypt_context.verify(
            senha_texto_claro,
            self.password,
            scheme="argon2",
        )

        if valid_hash:
            if crypt_context.needs_update(self.password):
                self.password = crypt_context.hash(senha_texto_claro)
                db.session.add(self)
                db.session.commit()

            return True

        return False
