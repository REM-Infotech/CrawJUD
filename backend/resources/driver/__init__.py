"""Gerenciador do webdriver para a execução dos bots."""

from .driver import BotDriver
from .web_element import WebElement

__all__ = ["BotDriver", "WebElement"]
