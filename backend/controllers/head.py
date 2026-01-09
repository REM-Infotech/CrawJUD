"""Implemente funcionalidades principais do bot CrawJUD."""

from __future__ import annotations

import logging
from abc import abstractmethod
from concurrent.futures import Future, ThreadPoolExecutor
from contextlib import suppress
from datetime import datetime
from pathlib import Path
from threading import Event
from time import sleep
from typing import TYPE_CHECKING, ClassVar, Self
from zoneinfo import ZoneInfo

from backend.base.task import CeleryTask
from backend.common.exceptions import StartError
from backend.common.exceptions._fatal import FatalError
from backend.extensions import celery
from backend.resources.driver import BotDriver
from backend.resources.iterators import BotIterator
from backend.resources.managers import CredencialManager, FileManager
from backend.resources.queues import PrintMessage, SaveError, SaveSuccess

if TYPE_CHECKING:
    from selenium.webdriver import Chrome as SeChrome
    from selenium.webdriver.support.wait import WebDriverWait
    from seleniumwire.webdriver import Chrome

    from typings import Dict


WORKDIR = Path.cwd()
MODULE_SPLIT_SIZE = 3
TZ = ZoneInfo("America/Sao_Paulo")
FORMAT_TIME = "%d-%m-%Y %H-%M-%S"

logger = logging.getLogger(__name__)
pool = ThreadPoolExecutor(1)

futures_shutdown: list[Future[None]] = []


class CrawJUD(CeleryTask):
    """Implemente a abstração do bot CrawJUD."""

    bots: ClassVar[dict[str, type[Self]]] = {}
    row: int = 0
    _total_rows: int = 0
    remaining: int = 0
    _name: str = ""

    @property
    def name(self) -> str:
        """Retorne o nome do bot CrawJUD."""
        return self._name

    @name.setter
    def name(self, val: str) -> None:
        self._name = val

    def shutdown_all(self) -> None:

        if hasattr(self, "driver") and not self.driver:
            window_handles = self.driver.window_handles
            if window_handles:
                self.driver.delete_all_cookies()
                self.driver.quit()

        if hasattr(self, "append_success"):
            with suppress(Exception):
                self.append_success.queue_save.shutdown()

        if hasattr(self, "append_error"):
            with suppress(Exception):
                self.append_error.queue_save.shutdown()

        kw = self.config
        kw["tipo_notificacao"] = "stop"
        celery.send_task("notifica_usuario", kwargs=kw)

    def setup(self, config: Dict) -> Self:
        """Configure o bot com as opções fornecidas.

        Args:
            config (Dict): Configurações do bot.

        Returns:
            Self: Instância configurada do bot.

        """
        self.config = config
        credenciais = config.get("credenciais", {})
        self.bot_stopped = Event()
        self.print_message = PrintMessage(self)
        self.append_success = SaveSuccess(self)
        self.append_error = SaveError(self)
        self.credenciais = CredencialManager(self)
        self.file_manager = FileManager(self)
        self.bot_driver = BotDriver(self)

        self.print_message("Robô inicializado!", message_type="success")

        self.credenciais.load_credenciais(credenciais)

        if credenciais.get("username") and config.get("sistema").upper() != "PJE":
            auth_ = self.auth()
            if not auth_:
                with suppress(Exception):
                    self.driver.quit()

                raise StartError(
                    message="Falha na autenticação do bot CrawJUD.",
                )

        if config.get("xlsx"):
            self.file_manager.download_files()
            self.frame = BotIterator(self)

        return self

    def finalizar_execucao(self) -> None:
        """Finalize a execução do bot e faça upload dos resultados."""
        with suppress(Exception):
            self.append_success.queue_save.shutdown()
            self.append_error.queue_save.shutdown()

            if not self.driver.is_closed:
                window_handles = self.driver.window_handles
                if window_handles:
                    self.driver.delete_all_cookies()
                    self.driver.quit()

        message = "Fim da execução"
        link = self.file_manager.upload_file()
        self.print_message(
            message=message,
            message_type="success",
            link=link,
        )

        sleep(5)

        self.print_message.queue_print_bot.shutdown()

    @abstractmethod
    def execution(self) -> None:
        """Execute as ações principais do bot.

        Raises:
            NotImplementedError: Método deve ser implementado
                pelas subclasses.

        """
        ...

    @abstractmethod
    def auth(self) -> None: ...

    @property
    def driver(self) -> SeChrome | Chrome:
        """Retorne o driver do navegador utilizado pelo bot."""
        return self.bot_driver.driver

    @property
    def wait(self) -> WebDriverWait[SeChrome | Chrome]:
        """Retorne o objeto de espera do driver do navegador."""
        return self.bot_driver.wait

    @property
    def output_dir_path(self) -> Path:
        """Retorne o caminho do diretório de saída do bot.

        Returns:
            Path: Caminho do diretório de saída criado.

        """
        out_dir = WORKDIR.joinpath("output", self.pid)
        out_dir.mkdir(parents=True, exist_ok=True)
        return out_dir

    @property
    def xlsx(self) -> str:
        """Retorne o caminho da planilha XLSX utilizada pelo bot."""
        return self.config.get("xlsx")

    @xlsx.setter
    def xlsx(self, val: str) -> None:
        self.config.update({"xlsx": val})

    @property
    def pid(self) -> str:
        """Retorne o identificador do processo do bot.

        Returns:
            str: Identificador do processo.

        """
        return self.config.get("pid")

    @property
    def anexos(self) -> list[str]:
        """Retorne a lista de anexos do bot.

        Returns:
            list[str]: Lista de caminhos dos anexos.

        """
        return self.config.get("anexos")

    @property
    def total_rows(self) -> int:
        """Retorne o total de linhas processadas pelo bot.

        Returns:
            int: Número total de linhas.

        """
        return self._total_rows

    @total_rows.setter
    def total_rows(self, value: int) -> None:
        self.remaining = value
        self._total_rows = value

    @property
    def now(self) -> str:
        """Retorne a data e hora atual formatada.

        Returns:
            str: Data e hora no formato 'dd-mm-YYYY HH-MM-SS'.

        """
        now_time = datetime.now(tz=TZ)
        return now_time.strftime(FORMAT_TIME)


class BotUtil:  # noqa: D101
    @staticmethod
    def on_done(fut: Future[None]) -> None:
        futures_shutdown.remove(fut)

    @staticmethod
    def create_thread_shutdown(bot: CrawJUD) -> None:

        sleep(5)
        future = pool.submit(bot.shutdown_all)
        futures_shutdown.append(future)
        future.add_done_callback(BotUtil.on_done)

    @staticmethod
    def logging_fatal_error(e: Exception, bot: CrawJUD) -> FatalError:
        exc = FatalError(e)
        if hasattr(bot, "print_message"):
            bot.print_message(
                message=f"Erro na execução do bot CrawJUD. {exc}",
                message_type="error",
            )
        logger.exception("Erro na execução do bot CrawJUD: %s", exc)  # noqa: LOG004
        return exc
