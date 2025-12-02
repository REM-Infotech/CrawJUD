"""Gerenciador do webdriver para a execução dos bots."""

from __future__ import annotations

from typing import TYPE_CHECKING

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.driver_cache import DriverCacheManager

from backend.task_manager.constants import WORKDIR
from backend.task_manager.constants.webdriver import (
    ARGUMENTS,
    PREFERENCES,
    SETTINGS,
)
from backend.task_manager.resources.driver.web_element import WebElementBot

if TYPE_CHECKING:
    from backend.task_manager.controllers.head import CrawJUD


class BotDriver:
    """Gerenciador do webdriver para a execução dos bots."""

    def __init__(self, bot: CrawJUD) -> None:
        """Inicialize o driver do bot com as configurações do sistema.

        Args:
            bot (CrawJUD): Instância do controlador do bot.

        """
        options = Options()
        user_data_dir = WORKDIR.joinpath("chrome-data", bot.pid)
        user_data_dir.mkdir(parents=True, exist_ok=True)
        user_data_dir.chmod(0o775)

        options.add_argument(f"--user-data-dir={user_data_dir!s}")

        for argument in ARGUMENTS:
            options.add_argument(argument)

        if "projudi" in bot.config.get("sistema"):
            options.add_argument("--incognito")

        download_dir = str(bot.output_dir_path)
        preferences = PREFERENCES
        preferences.update({
            "download.default_directory": download_dir,
            "printing.print_preview_sticky_settings.appState": SETTINGS,
        })

        options.add_experimental_option("prefs", preferences)

        for root, _, files in WORKDIR.joinpath(
            "chrome-extensions",
        ).walk():
            for file in filter(lambda x: x.endswith(".crx"), files):
                options.add_extension(str(root.joinpath(file)))

        cache_manager = DriverCacheManager()
        driver_manager = ChromeDriverManager(
            cache_manager=cache_manager,
        )
        service = Service(executable_path=driver_manager.install())
        self.driver = Chrome(options=options, service=service)

        webelement = WebElementBot.set_driver(self.driver)

        self.driver._web_element_cls = webelement
        self.wait = WebDriverWait(self.driver, 30)
