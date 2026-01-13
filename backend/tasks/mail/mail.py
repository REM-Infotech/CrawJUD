"""Implemente tarefas de envio de e-mail para notificações do sistema CrawJUD.

Este módulo define a task Celery responsável por enviar e-mails de
notificação de início e fim de execução de robôs, utilizando templates Jinja2
e integração com Flask-Mail.
"""

import logging
from contextlib import suppress
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING, ClassVar, Literal
from zoneinfo import ZoneInfo

from flask_mail import Message
from jinja2 import Environment

from backend.base.task import CeleryTask
from backend.common.exceptions._fatal import FatalError
from backend.models import Bots, ExecucoesBot, User
from backend.tasks.mail.templates import email_stop, mail_start

if TYPE_CHECKING:
    from flask_mail import Mail
    from flask_sqlalchemy import SQLAlchemy
    from jinja2.environment import Template as JinjaTemplate

    from typings import Any

PARENT_PATH = Path(__file__).parent.resolve()
TEMPLATES_PATH = PARENT_PATH.joinpath("templates")
TIMEZONE = ZoneInfo("America/Sao_Paulo")


logger = logging.getLogger("CrawJUD")
env = Environment(autoescape=True)
render_template = env.get_template


class MailTasks(CeleryTask):
    """Gerencie tarefas relacionadas ao envio de e-mails.

    Esta classe lida com notificações por e-mail para eventos de tarefas.
    """

    name = "notifica_usuario"

    TEMPLATE_START = render_template(mail_start)
    TEMPLATE_STOP = render_template(email_stop)

    notificacoes: ClassVar[dict[str, JinjaTemplate]] = {
        "start": TEMPLATE_START,
        "stop": TEMPLATE_STOP,
    }

    db: SQLAlchemy

    def __init__(self) -> None:  # noqa: D107
        from backend.extensions import app

        self.flaskapp = app
        self.db = app.extensions["sqlalchemy"]

        super().__init__()

    def run(
        self,
        id_execucao: str,
        bot_id: int,
        user_id: int,
        tipo_notificacao: Literal["start", "stop"],
        xlsx: str | None = None,
        **kwargs: str | Any,
    ) -> Literal["E-mail enviado com sucesso!"]:
        """Envie notificação de início de tarefa por e-mail.

        Args:
            app (Flask): Instância da aplicação Flask.
            id_execucao (str): Identificador do processo.
            bot_id (int): ID do bot.
            user_id (int): ID do usuário.
            xlsx (str | None): Caminho do arquivo XLSX (opcional).
            tipo_notificacao (Literal["start", "stop"]): Tipo de notificação.
            **kwargs: str | Any
        Returns:
            str: Mensagem de sucesso do envio do e-mail.

        """
        with self.flaskapp.app_context():
            url_web = self.flaskapp.config["WEB_URL"]

            with self.db.session.no_autoflush:
                self.user = self.query_user(user_id)
                self.bot = self.query_bot(bot_id)
                self.id_execucao = id_execucao
                self.tipo_notificacao = tipo_notificacao

                with suppress(Exception):
                    self.informacao_database()

                mail: Mail = self.flaskapp.extensions.get("mail")

                if mail:
                    try:
                        msg = Message(
                            subject="Notificação de Inicialização"
                            if tipo_notificacao == "start"
                            else "Notificação de Parada",
                            sender=mail.default_sender,
                            recipients=[self.user.email],
                        )

                        if not self.user.admin:
                            email_admin = self.db.session.query(User).filter(User.admin).all()
                            msg.cc = [email.email for email in email_admin[:3]]

                        template = self.notificacoes.get(tipo_notificacao)
                        msg.html = template.render(
                            display_name=self.bot.display_name,
                            id_execucao=id_execucao,
                            xlsx=xlsx,
                            url_web=url_web,
                            username=self.user.nome_usuario,
                        )

                        mail.send(msg)

                    except Exception as e:
                        exc = FatalError(e)
                        logger.exception("Erro de operação %r", repr(exc))
                        raise exc from e

                    return "E-mail enviado com sucesso!"

                return "Falha no envio do email"

    def informacao_database(self) -> None:
        """Gerencie início ou fim de execução de bot no banco.

        Args:
            app (Flask): Instância da aplicação Flask.
            bot_id (int): ID do bot a ser executado.
            user_id (int): ID do usuário responsável.
            id_execucao (str): Identificador do processo.
            operacao (Literal["start", "stop"]): Operação desejada.

        Returns:
            str: Mensagem de sucesso da operação.

        """
        now = datetime.now(tz=TIMEZONE)
        status_execucao = "Em Execução"
        if self.tipo_notificacao == "stop":
            # Finaliza execução existente pelo PID
            status_execucao = "Finalizado"
            execucao = self.query_execucao(self.id_execucao)
            if execucao:
                execucao.status = status_execucao
                execucao.data_fim = now
                self.db.session.commit()
                return

        # Cria uma nova execução do bot
        execucao = ExecucoesBot(
            id_execucao=self.id_execucao,
            status=status_execucao,
            data_inicio=now,
        )
        # Relaciona execução ao bot e usuário
        self.bot.execucoes.append(execucao)
        self.user.execucoes.append(execucao)
        self.db.session.add(execucao)
        self.db.session.commit()

    @classmethod
    def query_bot(cls, db: SQLAlchemy, bot_id: int) -> Bots | None:
        """Consulte e retorne um bot pelo ID informado.

        Args:
            db (SQLAlchemy): Instância do banco de dados SQLAlchemy.
            bot_id (int): Identificador do bot.

        Returns:
            Bots | None: Bot encontrado ou None se não existir.

        """
        return db.session.query(Bots).filter(Bots.Id == bot_id).first()

    def query_user(self, user_id: int) -> User | None:
        """Consulte e retorne um usuário pelo ID informado.

        Args:
            db (SQLAlchemy): Instância do banco de dados SQLAlchemy.
            user_id (int): Identificador do usuário.

        Returns:
            User | None: Usuário encontrado ou None se não existir.

        """
        return self.db.session.query(User).filter(User.Id == user_id).first()

    def query_execucao(self, id_execucao: str) -> ExecucoesBot | None:
        """Consulte e retorne uma execução pelo PID informado.

        Args:
            db (SQLAlchemy): Instância do banco de dados SQLAlchemy.
            id_execucao (str): Identificador do processo.

        Returns:
            ExecucoesBot | None: Execução encontrada ou None se não existir.

        """
        return (
            self.db.session
            .query(ExecucoesBot)
            .filter(ExecucoesBot.id_execucao == id_execucao)
            .first()
        )


__all__ = ["MailTasks"]
