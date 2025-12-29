"""Gerencie operações de busca automatizada usando Selenium.

Este módulo define a classe SearchBot para integrar
operações de busca com o bot principal CrawJUD.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from selenium.webdriver.chrome.webdriver import WebDriver
    from selenium.webdriver.support.wait import WebDriverWait
    from seleniumwire.webdriver import Chrome

    from backend.controllers.head import CrawJUD
    from backend.interfaces import BotData
    from backend.resources.queues.print_message import PrintMessage
    from backend.types_app import Dict


class SearchBot:
    """Gerencie operações de busca automatizada com Selenium.

    Args:
        bot (CrawJUD): Instância do bot principal.

    """

    def __init__(self, bot: CrawJUD) -> None:
        """Inicialize SearchBot com instância do bot principal.

        Args:
            bot (CrawJUD): Instância do bot principal.

        """
        self.bot = bot

    @property
    def driver(self) -> WebDriver | Chrome:
        """Obtenha o driver Selenium do bot principal."""
        return self.bot.driver

    @property
    def wait(self) -> WebDriverWait[WebDriver | Chrome]:
        """Retorne o objeto de espera do Selenium do bot principal."""
        return self.bot.wait

    @property
    def print_message(self) -> PrintMessage:
        """Obtenha o gerenciador de mensagens do bot principal."""
        return self.bot.print_message

    @property
    def bot_data(self) -> BotData:
        """Retorne os dados do bot principal."""
        return self.bot.bot_data

    @property
    def config(self) -> Dict:
        """Retorne as configurações do bot principal."""
        return self.bot.config
