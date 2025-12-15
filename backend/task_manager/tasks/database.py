"""Gerencie tarefas relacionadas ao banco de dados e execuções de bots.

Este módulo define tarefas para iniciar e finalizar execuções de bots,
utilizando integração com Celery e SQLAlchemy.
"""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Literal
from zoneinfo import ZoneInfo

from flask import Flask

from backend.task_manager.decorators import (
    SharedClassMethodTask,
)
from backend.task_manager.models import ExecucoesBot
from backend.task_manager.tasks.base import BotTasks

if TYPE_CHECKING:
    from flask import Flask
    from flask_sqlalchemy import SQLAlchemy


TIMEZONE = ZoneInfo("America/Sao_Paulo")


class DatabaseTasks(BotTasks):
    """Gerencie tarefas relacionadas ao banco de dados.

    Esta classe executa operações de controle de execuções de bots.
    """

    @classmethod
    @SharedClassMethodTask(name="informacao_database")
    def informacao_database(
        cls,
        app: Flask,
        bot_id: int,
        user_id: int,
        pid: str,
        operacao: Literal["start", "stop"],
    ) -> Literal["Operação de banco de dados concluída com sucesso!"]:
        """Gerencie início ou fim de execução de bot no banco.

        Args:
            app (Flask): Instância da aplicação Flask.
            bot_id (int): ID do bot a ser executado.
            user_id (int): ID do usuário responsável.
            pid (str): Identificador do processo.
            operacao (Literal["start", "stop"]): Operação desejada.

        Returns:
            str: Mensagem de sucesso da operação.

        """
        # Obtém instância do banco de dados
        db: SQLAlchemy = app.extensions["sqlalchemy"]
        # Busca usuário e bot relacionados
        user = cls.query_user(db, user_id)
        bot = cls.query_bot(db, bot_id)

        now = datetime.now(tz=TIMEZONE)
        if operacao == "start":
            # Cria uma nova execução do bot
            execucao = ExecucoesBot(
                pid=pid,
                status="Em Execução",
                data_inicio=now,
            )
            # Relaciona execução ao bot e usuário
            bot.execucoes.append(execucao)
            user.execucoes.append(execucao)
            db.session.add(execucao)
            db.session.commit()

        elif operacao == "stop":
            # Finaliza execução existente pelo PID
            execucao = cls.query_execucao(db, pid)
            if execucao:
                execucao.status = "Finalizado"
                execucao.data_fim = now
                db.session.commit()

        return "Operação de banco de dados concluída com sucesso!"
