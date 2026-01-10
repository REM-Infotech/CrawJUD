"""Gerenciador do webdriver para a execução dos bots."""

from __future__ import annotations

from pathlib import Path
from threading import Event
from typing import TYPE_CHECKING, TypedDict, Unpack

from selenium.webdriver import Chrome as SeChromeDriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from seleniumwire.webdriver import Chrome as SeWireChrome
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.driver_cache import DriverCacheManager

from backend.resources.driver.web_element import WebElement

from .constants import ARGUMENTS, PREFERENCES, SETTINGS

if TYPE_CHECKING:
    from backend.controllers.head import CrawJUD


WORKDIR = Path.cwd()


class ChromeDriverKwargs(TypedDict):  # noqa: D101
    options: Options
    service: Service


class SeleniumWireOptions(TypedDict):  # noqa: D101
    addr: str
    port: int
    exclude_hosts: list[str]
    standalone: bool


class Chrome(SeChromeDriver):  # noqa: D101
    def __init__(  # noqa: D107
        self,
        options: Options = None,
        service: Service = None,
        *,
        keep_alive: bool = True,
    ) -> None:

        self._event_driver = Event()
        super().__init__(options, service, keep_alive)

    def quit(self) -> None:
        self._event_driver.set()
        return super().quit()

    @property
    def is_closed(self) -> bool:
        return self._event_driver.is_set()


class SeleniumWireChrome(SeWireChrome):  # noqa: D101
    def __init__(  # noqa: D107
        self,
        *,
        seleniumwire_options: SeleniumWireOptions = None,
        **kwargs: Unpack[ChromeDriverKwargs],
    ) -> None:
        self._event_driver = Event()
        super().__init__(seleniumwire_options=seleniumwire_options, **kwargs)

    def quit(self) -> None:
        self._event_driver.set()
        return super().quit()

    @property
    def is_closed(self) -> bool:
        return self._event_driver.is_set()


class BotDriver:
    """Gerenciador do webdriver para a execução dos bots."""

    def __init__(self, bot: CrawJUD) -> None:
        """Inicialize o driver do bot com as configurações do sistema.

        Args:
            bot (CrawJUD): Instância do controlador do bot.

        """
        options = Options()
        user_data_dir = WORKDIR.joinpath("chrome-data", bot.id_execucao)
        user_data_dir.mkdir(parents=True, exist_ok=True)
        user_data_dir.chmod(0o775)

        options.add_argument(f"--user-data-dir={user_data_dir!s}")

        for argument in ARGUMENTS:
            options.add_argument(argument)

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
        if bot.config.get("sistema").upper() != "PJE":
            self.driver = Chrome(options=options, service=service)

        elif bot.config.get("sistema").upper() == "PJE":
            self.driver = SeleniumWireChrome(options=options, service=service)

        webelement = WebElement.set_driver(self.driver)

        self.driver._web_element_cls = webelement  # noqa: SLF001
        self.wait = WebDriverWait(self.driver, 30)
