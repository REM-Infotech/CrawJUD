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

from celery import shared_task
from selenium.webdriver.common.by import By

from backend.base.task import CeleryTask
from backend.common.exceptions import StartError
from backend.common.raises import raise_execution_error
from backend.extensions import celery
from backend.resources.driver import BotDriver, WebElement
from backend.resources.iterators import BotIterator
from backend.resources.managers import CredencialManager, FileManager
from backend.resources.queues import PrintMessage, SaveError, SaveSuccess

if TYPE_CHECKING:
    from selenium.webdriver import Chrome as SeChrome
    from selenium.webdriver.support.wait import WebDriverWait
    from seleniumwire.webdriver import Chrome

    from backend.dicionarios import ConfigArgsRobo
    from backend.tasks.bots.busca_processual.projudi import BuscaProcessual
    from backend.tasks.bots.capa.projudi import Capa


WORKDIR = Path.cwd()
MODULE_SPLIT_SIZE = 3
TZ = ZoneInfo("America/Sao_Paulo")
FORMAT_TIME = "%d-%m-%Y %H-%M-%S"

logger = logging.getLogger(__name__)
pool = ThreadPoolExecutor(1)

futures_shutdown: list[Future[None]] = []


EMPTY_CONFIG = {
    "id_execucao": "",
    "sistema": "",
    "categoria": "",
    "credenciais": {
        "username": "",
        "password": "",
        "otp": "",
        "certificado": "",
        "nome_certificado": "",
    },
}


class CrawJUD(CeleryTask):
    """Implemente a abstração do bot CrawJUD."""

    bots: ClassVar[dict[str, type[CrawJUD]]] = {}
    row: int = 0
    _total_rows: int = 0
    remaining: int = 0
    name: str = ""
    config: ClassVar[ConfigArgsRobo] = EMPTY_CONFIG

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

    def setup(self, config: ConfigArgsRobo) -> Self:
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
        out_dir = WORKDIR.joinpath("output", self.id_execucao)
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
    def id_execucao(self) -> str:
        """Retorne o identificador do processo do bot.

        Returns:
            str: Identificador do processo.

        """
        return self.config.get("id_execucao")

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

    def __init_subclass__(cls) -> None:  # noqa: D105

        if hasattr(cls, "name") and cls.name:
            cls.bots[cls.name] = cls

    def select2(self, seletor: WebElement, opcao: str) -> None:

        items = seletor.find_elements(By.TAG_NAME, "option")
        opt_itens: dict[str, str] = {}

        for item in items:
            value_item = item.get_attribute("value")
            command = "return $(arguments[0]).text();"
            text_item = self.driver.execute_script(command, item)
            text_item = " ".join([
                item for item in str(text_item).strip().split(" ") if item
            ]).upper()
            opt_itens.update({text_item: value_item})

        to_search = " ".join(opcao.split(" ")).upper()
        value_opt = opt_itens.get(to_search)

        if value_opt:
            command = """
            const selector = $(arguments[0]);
            selector.val([arguments[1]]);
            selector.trigger("change");
            """
            self.parent.execute_script(
                command,
                seletor,
                value_opt,
            )
            return

        raise_execution_error(
            message=f'Opção "{to_search}" não encontrada!',
        )


@shared_task(name="tarefa-prototipo")
def tarefa_prototipo(config: ConfigArgsRobo) -> None:  # noqa: D103

    config.update({
        "sistema": "projudi",
    })
    bot: BuscaProcessual = CrawJUD.bots["busca_processual_projudi"]()
    frame = bot.run(config)

    bot: Capa = CrawJUD.bots["capa_projudi"]()
    bot.frame = frame
    _results = bot.run(config)
