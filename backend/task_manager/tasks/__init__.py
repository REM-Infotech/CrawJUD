"""Task module for Celery."""

from backend.task_manager import bots
from backend.task_manager.tasks import database, mail

__all__ = ["bots", "database", "mail"]
