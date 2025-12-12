"""Gerencie tarefas de envio de e-mails para notificações.

Este pacote lida com templates e envio de e-mails para eventos de tarefas.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Literal

from flask import Flask
from flask_mail import Message

from backend.api.models import User
from backend.task_manager.decorators import (
    SharedClassMethodTask as SharedClassMethodTask,
)
from backend.task_manager.tasks.base import BotTasks

if TYPE_CHECKING:
    from celery import Celery
    from flask import Flask
    from flask_mail import Mail


class MailTasks(BotTasks):
    """Gerencie tarefas relacionadas ao envio de e-mails.

    Esta classe lida com notificações por e-mail para eventos de tarefas.
    """

    @classmethod
    @SharedClassMethodTask(name="notifica_usuario")
    def notificacao_inicio(
        cls,
        app: Flask,
        pid: str,
        bot_id: int,
        user_id: int,
        tipo_notificacao: Literal["start", "stop"],
        xlsx: str | None = None,
    ) -> Literal["E-mail enviado com sucesso!"]:
        """Envie notificação de início de tarefa por e-mail.

        Args:
            app (Flask): Instância da aplicação Flask.
            pid (str): Identificador do processo.
            bot_id (int): ID do bot.
            user_id (int): ID do usuário.
            xlsx (str | None): Caminho do arquivo XLSX (opcional).
            tipo_notificacao (Literal["start", "stop"]): Tipo de notificação.

        Returns:
            str: Mensagem de sucesso do envio do e-mail.

        """
        mail: Mail = app.extensions["mail"]
        url_web = app.config["WEB_URL"]
        celery: Celery = app.extensions["celery"]

        db = cls.sqlalchemy_instance(app)
        user = cls.query_user(db, user_id)
        bot = cls.query_bot(db, bot_id)

        celery.send_task(
            "informacao_database",
            kwargs={
                "pid": pid,
                "bot_id": bot.Id,
                "user_id": user.Id,
                "operacao": tipo_notificacao,
            },
        )

        msg = Message(
            subject="Notificação de Inicialização"
            if tipo_notificacao == "start"
            else "Notificação de Parada",
            sender=mail.default_sender,
            recipients=[user.email],
        )

        if not user.admin:
            email_admin = db.session.query(User).filter(User.admin).all()
            msg.cc = [email.email for email in email_admin[:3]]

        template = cls.notificacoes.get(tipo_notificacao)
        msg.html = template.render(
            display_name=bot.display_name,
            pid=pid,
            xlsx=xlsx,
            url_web=url_web,
            username=user.nome_usuario,
        )

        mail.send(msg)

        return "E-mail enviado com sucesso!"
