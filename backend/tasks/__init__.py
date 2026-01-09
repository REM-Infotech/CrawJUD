"""Inicialize o pacote de tarefas do sistema CrawJUD.

Este módulo permite o uso de submódulos relacionados a tarefas,
como envio de e-mails, agendamento e execução de jobs.
"""

from .register import register_tasks

__all__ = ["register_tasks"]
