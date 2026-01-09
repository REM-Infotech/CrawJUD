"""Defina templates de e-mail para notificações de início e fim de execução.

Este módulo utiliza Jinja2 para gerar mensagens HTML dinâmicas enviadas pelo sistema.
Inclui templates para notificação de inicialização e finalização de robôs.
"""

from jinja2.environment import Template

mail_start: Template = Template(
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

email_stop: Template = Template(
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


__all__ = ["email_stop", "mail_start"]
