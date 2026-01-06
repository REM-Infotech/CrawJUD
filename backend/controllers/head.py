"""Implemente funcionalidades principais do bot CrawJUD."""

from __future__ import annotations

import logging
from abc import abstractmethod
from concurrent.futures import Future, ThreadPoolExecutor
from contextlib import suppress
from datetime import datetime
from threading import Event
from time import sleep
from typing import TYPE_CHECKING, ClassVar, Self
from warnings import warn
from zoneinfo import ZoneInfo

from clear import clear
from dotenv import load_dotenv

from backend.common.exceptions import StartError
from backend.common.exceptions._fatal import FatalError
from backend.common.exceptions._file import ArquivoNaoEncontradoError
from backend.extensions import celery
from backend.resources.driver import BotDriver
from backend.resources.iterators import BotIterator
from backend.resources.managers.credencial_manager import (
    CredencialManager,
)
from backend.resources.managers.file_manager import FileManager
from backend.resources.queues.file_operation import (
    SaveError,
    SaveSuccess,
)
from backend.resources.queues.print_message import PrintMessage
from backend.task_manager.constants import WORKDIR
from backend.task_manager.decorators import SharedTask

if TYPE_CHECKING:
    from pathlib import Path

    from selenium.webdriver.chrome.webdriver import WebDriver
    from selenium.webdriver.support.wait import WebDriverWait
    from seleniumwire.webdriver import Chrome

    from backend.types_app import AnyType, Dict

MODULE_SPLIT_SIZE = 3
TZ = ZoneInfo("America/Sao_Paulo")
FORMAT_TIME = "%d-%m-%Y %H-%M-%S"

logger = logging.getLogger(__name__)
pool = ThreadPoolExecutor(1)

futures_shutdown: list[Future[None]] = []


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

        if hasattr(self, "driver") and not self.driver.is_closed:
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

                raise StartError(message="Falha na autenticação do bot CrawJUD.")

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


@SharedTask(name="crawjud")
def start_bot(config: Dict) -> None:
    """Inicie o bot CrawJUD com a configuração fornecida.

    Args:
        config (Dict): Configuração do bot.

    Returns:
        None: Não retorna valor.

    """
    load_dotenv()

    try:
        bot_nome = f"{config['categoria']}_{config['sistema']}"
        bot = CrawJUD.bots.get(bot_nome)
        if not bot:
            bot_nome = f"{config['sistema']}_{config['categoria']}"
            bot = CrawJUD.bots[bot_nome]

        bot = bot()
        bot.setup(config=config)
        bot.execution()
        BotUtil.create_thread_shutdown(bot)

    except (ArquivoNaoEncontradoError, FatalError) as e:
        exc = BotUtil.logging_fatal_error(e, bot)
        BotUtil.create_thread_shutdown(bot)

        raise exc from e

    except KeyError as e:
        clear()

        class Dummy(CrawJUD): ...

        config["sistema"] = "PJE"

        bot = Dummy().setup(config=config)
        exc = BotUtil.logging_fatal_error(e, bot)
        BotUtil.create_thread_shutdown(bot)
        raise exc from e

    except Exception as e:
        clear()

        exc = BotUtil.logging_fatal_error(e, bot)
        BotUtil.create_thread_shutdown(bot)

        raise exc from e
