"""Implemente funcionalidades principais do bot CrawJUD."""

from __future__ import annotations

import logging
from abc import abstractmethod
from contextlib import suppress
from datetime import datetime
from threading import Event
from time import sleep
from traceback import format_exception
from typing import TYPE_CHECKING, ClassVar, Self
from warnings import warn
from zoneinfo import ZoneInfo

from clear import clear

from backend.task_manager.constants import WORKDIR
from backend.task_manager.decorators import SharedTask
from backend.task_manager.resources.driver import BotDriver
from backend.task_manager.resources.iterators import BotIterator
from backend.task_manager.resources.managers.credencial_manager import (
    CredencialManager,
)
from backend.task_manager.resources.managers.file_manager import FileManager
from backend.task_manager.resources.queues.file_operation import (
    SaveError,
    SaveSuccess,
)
from backend.task_manager.resources.queues.print_message import PrintMessage

if TYPE_CHECKING:
    from pathlib import Path

    from selenium.webdriver.chrome.webdriver import WebDriver
    from selenium.webdriver.support.wait import WebDriverWait
    from seleniumwire.webdriver import Chrome

    from backend.api.types_app import AnyType
    from backend.task_manager.types_app import Dict

MODULE_SPLIT_SIZE = 3
TZ = ZoneInfo("America/Sao_Paulo")
FORMAT_TIME = "%d-%m-%Y %H-%M-%S"

logger = logging.getLogger(__name__)


class FatalError(Exception):
    """Exceção fatal na execução do bot CrawJUD."""

    message: ClassVar[str] = "Fatal error in CrawJUD bot execution."

    def __init__(self, exc: Exception, *args: AnyType) -> None:
        """Initialize FatalError with the given exception.

        Args:
            exc (Exception): The exception that caused the fatal error.
            *args (AnyType): Additional arguments to pass to the base Exception.

        """
        # Store only the string representation to ensure picklability
        self._exc_str = repr(exc)
        self._exc_type = type(exc).__name__
        self._exc_msg = str(exc)
        self._traceback = "".join(format_exception(exc))
        self._format()
        super().__init__(*args)

    def _format(self) -> None:
        self.message = self._traceback

    def __str__(self) -> str:
        """Return the string representation of the FatalError."""
        return self.message

    def __repr__(self) -> str:
        """Return the string representation of the FatalError for debugging."""
        return f"FatalException(type={self._exc_type}, message={self._exc_msg})"

    def __reduce__(self) -> tuple[type[Self], tuple[Exception]]:  # noqa: D105
        # Provide a way for pickle to reconstruct the object
        return (
            self.__class__,
            (Exception(self._exc_msg),),  # reconstruct with a generic Exception
        )

    def __getstate__(self) -> dict[str, AnyType]:  # noqa: D105
        # Only store pickleable attributes
        return {
            "_exc_str": self._exc_str,
            "_exc_type": self._exc_type,
            "_exc_msg": self._exc_msg,
            "_traceback": self._traceback,
            "message": self.message,
        }

    def __setstate__(self, state: dict[str, AnyType]) -> None:  # noqa: D105
        self._exc_str = state["_exc_str"]
        self._exc_type = state["_exc_type"]
        self._exc_msg = state["_exc_msg"]
        self._traceback = state["_traceback"]
        self.message = state["message"]


class CrawJUD:
    """Implemente a abstração do bot CrawJUD."""

    bots: ClassVar[dict[str, type[Self]]] = {}
    row: int = 0
    _total_rows: int = 0
    remaining: int = 0

    @property
    @abstractmethod
    def name(self) -> str:
        """Retorne o nome do bot CrawJUD."""

    def shutdown_all(self) -> None:
        if hasattr(self, "append_success"):
            with suppress(Exception):
                self.append_success.queue_save.shutdown()

        if hasattr(self, "append_error"):
            with suppress(Exception):
                self.append_error.queue_save.shutdown()

        if hasattr(self, "driver"):
            with suppress(Exception):
                window_handles = self.driver.window_handles
                if window_handles:
                    self.driver.delete_all_cookies()
                    self.driver.quit()

    @classmethod
    def __subclasshook__(cls, *args: AnyType, **kwargs: AnyType) -> None:
        """Registre subclasses do CrawJUD automaticamente."""
        if not hasattr(cls, "name"):
            warn(
                "Atributo 'name' não definido na subclasse CrawJUD.",
                stacklevel=2,
            )

        return True

    def __init_subclass__(cls) -> None:
        """Inicialize subclasses do CrawJUD e registre bots.

        Args:
            cls (type): Subclasse de CrawJUD.


        """
        if not hasattr(cls, "name"):
            return

        CrawJUD.bots[cls.name] = cls

    def setup(self, config: Dict) -> Self:
        """Configure o bot com as opções fornecidas.

        Args:
            config (Dict): Configurações do bot.

        Returns:
            Self: Instância configurada do bot.

        """
        self.config = config
        self.bot_stopped = Event()
        self.print_message = PrintMessage(self)
        self.append_success = SaveSuccess(self)
        self.append_error = SaveError(self)
        self.credenciais = CredencialManager(self)
        self.file_manager = FileManager(self)
        self.bot_driver = BotDriver(self)

        self.print_message("Robô inicializado!", message_type="success")

        if config.get("credenciais"):
            self.credenciais.load_credenciais(
                self.config.get("credenciais"),
            )
            if not self.auth():
                with suppress(Exception):
                    self.driver.quit()

        if config.get("planilha_xlsx"):
            self.file_manager.download_files()
            self.frame = BotIterator(self)

        return self

    def finalizar_execucao(self) -> None:
        """Finalize a execução do bot e faça upload dos resultados."""
        with suppress(Exception):
            self.append_success.queue_save.shutdown()
            self.append_error.queue_save.shutdown()
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

    @property
    def driver(self) -> WebDriver | Chrome:
        """Retorne o driver do navegador utilizado pelo bot."""
        return self.bot_driver.driver

    @property
    def wait(self) -> WebDriverWait[WebDriver | Chrome]:
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
    def planilha_xlsx(self) -> str:
        """Retorne o caminho da planilha XLSX utilizada pelo bot."""
        return self.config.get("planilha_xlsx")

    @planilha_xlsx.setter
    def planilha_xlsx(self, val: str) -> None:
        self.config.update({"planilha_xlsx": val})

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


@SharedTask(name="crawjud")
def start_bot(config: Dict) -> None:
    """Inicie o bot CrawJUD com a configuração fornecida.

    Args:
        config (Dict): Configuração do bot.

    Returns:
        None: Não retorna valor.

    """
    try:
        bot_nome = f"{config['categoria']}_{config['sistema']}"
        bot = CrawJUD.bots.get(bot_nome)
        bot = bot().setup(config=config)

        bot.execution()

        bot.shutdown_all()

    except KeyError as e:
        clear()

        class Dummy(CrawJUD): ...

        bot = Dummy().setup(config=config)

        exc = FatalError(e)
        bot.print_message(
            message=f"Erro na execução do bot CrawJUD. {exc}",
            message_type="error",
        )

        logger.exception("Erro na execução do bot CrawJUD: %s", exc)
        sleep(5)
        bot.shutdown_all()
        raise exc from e

    except Exception as e:
        clear()

        exc = FatalError(e)

        if hasattr(bot, "print_message"):
            bot.print_message(
                message=f"Erro na execução do bot CrawJUD. {exc}",
                message_type="error",
            )

        logger.exception("Erro na execução do bot CrawJUD: %s", exc)

        sleep(5)
        bot.shutdown_all()

        raise exc from e
