"""Gerencie autenticação e recursos relacionados a bots.

Este módulo fornece a classe AutenticadorBot para facilitar
operações de autenticação e acesso a recursos do bot.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from selenium.webdriver.chrome.webdriver import WebDriver
    from selenium.webdriver.support.wait import WebDriverWait
    from seleniumwire.webdriver import Chrome

    from backend.resources.managers.credencial_manager import (
        CredencialManager,
    )
    from backend.resources.queues.print_message import PrintMessage
    from backend.task_manager.controllers.head import CrawJUD


class AutenticadorBot:
    """Gerencie autenticação de bots no sistema.

    Args:
        bot (CrawJUD): Instância do bot principal.

    """

    def __init__(self, bot: CrawJUD) -> None:
        """Inicialize o autenticador com uma instância do bot.

        Args:
            bot (CrawJUD): Instância do bot principal.

        """
        self.bot = bot

    @property
    def driver(self) -> WebDriver | Chrome:
        """Retorne o driver do bot para automação web."""
        return self.bot.driver

    @property
    def wait(self) -> WebDriverWait[WebDriver | Chrome]:
        """Obtenha o objeto de espera do driver do bot."""
        return self.bot.wait

    @property
    def print_message(self) -> PrintMessage:
        """Obtenha o gerenciador de mensagens do bot."""
        return self.bot.print_message

    @property
    def bot_data[T](self) -> T:
        """Retorne os dados do bot para uso interno."""
        return self.bot.bot_data

    @property
    def credenciais(self) -> CredencialManager:
        """Obtenha o gerenciador de credenciais do bot."""
        return self.bot.credenciais
