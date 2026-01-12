from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Column, DateTime, Integer, String

from backend.extensions import db

if TYPE_CHECKING:
    from datetime import datetime


rel = db.relationship


class Processo(db.Model):
    __tablename__ = "processos"
    Id: int = Column("id", Integer, primary_key=True)
    NUMERO_PROCESSO: str = Column("numero_processo", String(length=64), nullable=False)
    DATA_DISTRIBUICAO: datetime = Column("data_distribuicao", DateTime(timezone=True))
    ESTADO: str = Column("estado", String(length=64), nullable=False)
    COMARCA: str = Column("comarca", String(length=64), nullable=False)
    FORO: str = Column("foro", String(length=64), nullable=False)
    VARA: str = Column("vara", String(length=64), nullable=False)
