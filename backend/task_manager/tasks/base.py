"""Gerencie tarefas e utilitários para bots e execuções.

Este módulo fornece classes e funções para manipular bots,
usuários, execuções e templates de e-mail.
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, ClassVar
from zoneinfo import ZoneInfo

from jinja2 import Environment, FileSystemLoader
from jinja2.environment import Template as JinjaTemplate

from backend.models import Bots, ExecucoesBot, User

if TYPE_CHECKING:
    from flask import Flask
    from flask_sqlalchemy import SQLAlchemy


PARENT_PATH = Path(__file__).parent.resolve()
TEMPLATES_PATH = PARENT_PATH.joinpath("templates")
TIMEZONE = ZoneInfo("America/Sao_Paulo")


mail_start = JinjaTemplate(
    """
<h1>Notificação de Inicialização - PID {{ pid }}</h1>
<p>Prezado {{ username }},</p>
<p>Sua execução foi inicializada com sucesso!</p>
<ul>
    <li>Robô: {{display_name}}</li>
    <li>Planilha: {{xlsx}}</li>
</ul>
<p>Acompanhe a execução em:
    <b>
        <a href="{{ url_web }}/logs/{{ pid }}">Nosso Sistema</a>
    </b>
</p>
<p>Por favor,
    <b>Não responder este email.</b>
</p>
""",
)

email_stop = JinjaTemplate(
    """
<h1>Notificação de Finalização - PID {{pid}}</h1>
<p>Prezado {{ username }},</p>
<p>Sua execução foi finalizada com sucesso!</p>
<ul>
    <li>Robô: {{display_name}}</li>
    <li>Planilha: {{xlsx}}</li>
</ul>
<p>Baixe o resultado
    <b>
        <a href="crawjud://download_execucao/{{pid}}">Clicando aqui</a>
    </b>
</p>
<p>Por favor,
    <b>Não responda a este e-mail</b>
</p>
""",
)


class BotTasks:
    """Gerencie tarefas relacionadas a bots e consultas ao banco.

    Esta classe fornece métodos utilitários para manipular bots,
    usuários e execuções, além de gerenciar templates de e-mail.
    """

    env = Environment(loader=FileSystemLoader(TEMPLATES_PATH), autoescape=True)
    render_template = env.get_template
    TEMPLATE_START = render_template(mail_start)
    TEMPLATE_STOP = render_template(email_stop)

    notificacoes: ClassVar[dict[str, JinjaTemplate]] = {
        "start": TEMPLATE_START,
        "stop": TEMPLATE_STOP,
    }

    @classmethod
    def sqlalchemy_instance(cls, app: Flask) -> SQLAlchemy:
        """Retorne a instância do SQLAlchemy do app Flask fornecido.

        Args:
            app (Flask): Instância da aplicação Flask.

        Returns:
            SQLAlchemy: Instância do SQLAlchemy associada ao app.

        """
        return app.extensions["sqlalchemy"]

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

    @classmethod
    def query_user(cls, db: SQLAlchemy, user_id: int) -> User | None:
        """Consulte e retorne um usuário pelo ID informado.

        Args:
            db (SQLAlchemy): Instância do banco de dados SQLAlchemy.
            user_id (int): Identificador do usuário.

        Returns:
            User | None: Usuário encontrado ou None se não existir.

        """
        return db.session.query(User).filter(User.Id == user_id).first()

    @classmethod
    def query_execucao(cls, db: SQLAlchemy, pid: str) -> ExecucoesBot | None:
        """Consulte e retorne uma execução pelo PID informado.

        Args:
            db (SQLAlchemy): Instância do banco de dados SQLAlchemy.
            pid (str): Identificador do processo.

        Returns:
            ExecucoesBot | None: Execução encontrada ou None se não existir.

        """
        return db.session.query(ExecucoesBot).filter(ExecucoesBot.pid == pid).first()
