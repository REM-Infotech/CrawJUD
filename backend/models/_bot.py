"""Modulo de controle da model bots."""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar, Literal

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import Mapped  # noqa: TC002

from backend.extensions import db

if TYPE_CHECKING:
    from datetime import datetime

    from backend.models._users import LicenseUser, User

rel = db.relationship

type _TableArgs = dict[Literal["extend_existing"], bool]


class Bots(db.Model):
    __tablename__ = "bots"
    __table_args__: ClassVar[_TableArgs] = {"extend_existing": True}
    Id: int = Column("id", Integer, primary_key=True)
    display_name: str = Column(String(64), nullable=False)
    sistema: str = Column(String(16), nullable=False)
    categoria: str = Column(String(32), nullable=False)
    configuracao_form: str = Column(
        String(64),
        nullable=False,
        default="",
    )
    descricao: str = Column(
        "descricao",
        String(length=256),
        nullable=False,
    )

    license_id: int = Column(Integer, db.ForeignKey("licencas.id"))
    license_: Mapped[LicenseUser] = rel(back_populates="bots")

    execucoes: Mapped[list[ExecucoesBot]] = rel(back_populates="bot")


class ExecucoesBot(db.Model):
    """Model de execuções dos bots."""

    __tablename__ = "execucoes"
    __table_args__: ClassVar[_TableArgs] = {"extend_existing": True}

    Id: int = Column("id", Integer, primary_key=True)
    id_execucao: str = Column(String(length=64), nullable=False)
    status: str = Column("status", String(length=64), nullable=False)

    data_inicio: datetime = Column(DateTime(), nullable=True)
    data_fim: datetime = Column(DateTime(), nullable=True)

    user_id: int = Column(Integer, db.ForeignKey("usuarios.id"))
    usuario: Mapped[User] = rel(back_populates="execucoes")

    bot_id: int = Column(Integer, db.ForeignKey("bots.id"))
    bot: Mapped[Bots] = rel(back_populates="execucoes")


class CredenciaisRobo(db.Model):
    """Credenciais Bots Model."""

    __tablename__ = "credenciais_robo"
    __table_args__: ClassVar[_TableArgs] = {"extend_existing": True}

    Id: int = Column("id", Integer, primary_key=True)
    nome_credencial: str = Column(
        "nome_credencial",
        String(length=64),
        nullable=False,
    )
    sistema: str = Column("sistema", String(length=64), nullable=False)
    login_metodo: str = Column(
        "metodo_login",
        String(length=12),
        default="pw",
        nullable=False,
    )
    rastreio: str = Column("rastreio", String(length=64), nullable=False)
    license_id: int = Column(Integer, db.ForeignKey("licencas.id"))
    license_: Mapped[LicenseUser] = rel(back_populates="credenciais")


class Processo(db.Model):
    __tablename__ = "processos"
    Id: int = Column("id", Integer, primary_key=True)
    NUMERO_PROCESSO: str = Column("numero_processo", String(length=64), nullable=False)
    DATA_DISTRIBUICAO: datetime = Column("data_distribuicao", DateTime(timezone=True))
