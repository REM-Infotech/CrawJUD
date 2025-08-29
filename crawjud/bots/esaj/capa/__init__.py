"""Module: capa.

Extract and manage process details from esaj by scraping and formatting data.
"""

from __future__ import annotations

import shutil
import time
from contextlib import suppress
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING, ClassVar

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec

from crawjud.bots.esaj.capa._1 import PrimeiraInstancia
from crawjud.bots.esaj.capa._2 import SegundaInstancia
from crawjud.common import _raise_execution_error
from crawjud.common.exceptions.bot import ExecutionError
from crawjud.custom.task import ContextTask
from crawjud.decorators import shared_task
from crawjud.decorators.bot import wrap_cls

if TYPE_CHECKING:
    from datetime import datetime

    from selenium.webdriver.remote.webelement import WebElement  # noqa: F401

    from crawjud.interfaces.types import ListPartes, ProcessInfo


@shared_task(name="esaj.capa", bind=True, base=ContextTask)
@wrap_cls
class Capa(PrimeiraInstancia, SegundaInstancia):
    """Extract process information from Esaj and populate structured data.

    This class extends CrawJUD to click through information panels,
    extract process data and participant details, and format them accordingly.
    """

    to_add_partes: ClassVar[list[ProcessInfo]] = []
    to_add_assuntos: ClassVar[list[ProcessInfo]] = []
    to_add_processos: ClassVar[list[ProcessInfo]] = []
    to_add_audiencias: ClassVar[list[ProcessInfo]] = []
    to_add_representantes: ClassVar[list[ProcessInfo]] = []

    list_partes: ClassVar[ListPartes] = []

    def execution(self) -> None:
        """Execute the main processing loop to extract process information.

        Iterates over each data row and queues process data extraction.
        """
        frame = self.frame

        self._total_rows = len(frame)

        for pos, value in enumerate(frame):
            if self.event_stop_bot.is_set():
                break

            self.row = pos + 1
            self.bot_data = value

            with suppress(Exception):
                if self.driver.title.lower() == "a sessao expirou":
                    self.auth()

            try:
                self.queue()

            except ExecutionError as e:
                message_error = str(e)

                self.print_msg(
                    message=f"{message_error}.",
                    type_log="error",
                )

                self.bot_data.update({"MOTIVO_ERRO": message_error})
                self.append_error(self.bot_data)

                self.message_error = None

        for to_save, sheet_name in [
            (self.to_add_processos_primeiro_grau, "Capa Primeiro Grau"),
            (self.to_add_processos_segundo_grau, "Capa Segundo Grau"),
            (self.to_add_partes, "Partes"),
            (self.to_add_representantes, "Representantes"),
        ]:
            self.queue_save_xlsx.put({
                "to_save": to_save,
                "sheet_name": sheet_name,
            })

        self.finalize_execution()

    def queue(self) -> None:
        """Handle the process information extraction queue by refreshing the driver.

        Raises:
            ExecutionError: If the process is not found or extraction fails.

        """
        try:
            driver = self.driver
            bot_data = self.bot_data

            self.print_msg(
                message=f"Buscando processo {bot_data['NUMERO_PROCESSO']}",
                row=self.row,
                type_log="log",
            )

            search = self.search()
            trazer_copia = bot_data.get("TRAZER_COPIA", "não")
            if not search:
                self.print_msg(
                    message="Processo não encontrado.",
                    row=self.row,
                    type_log="error",
                )
                return

            self.print_msg(
                message="Processo encontrado! Extraindo informações...",
                row=self.row,
                type_log="info",
            )

            driver.refresh()
            data = self.get_process_informations()

            if trazer_copia and trazer_copia.lower() == "sim":
                data = self.copia_pdf(data)

            self.print_msg(
                message="Informações extraídas com sucesso!",
                row=self.row,
                type_log="success",
            )

        except ExecutionError as e:
            raise ExecutionError(exc=e) from e

    def get_process_informations(self) -> None:
        """Extrai informações detalhadas do processo da página atual do esaj."""
        try:
            bot_data = self.bot_data
            numero_processo = bot_data.get("NUMERO_PROCESSO")

            callables = {"1": self.primeiro_grau, "2": self.segundo_grau}

            callables[str(bot_data.get("GRAU", "1"))](
                numero_processo=numero_processo,
            )

        except (ExecutionError, Exception):
            _raise_execution_error("Erro ao executar operação")

    def primeiro_grau(self, numero_processo: str) -> None:
        process_info: ProcessInfo = {"Número do processo": numero_processo}
        process_info.update(self._informacoes_gerais_primeiro_grau())
        process_info.update(self._info_processual_primeiro_grau())

        self._partes_primeiro_grau(numero_processo=numero_processo)
        self.to_add_processos_primeiro_grau.append(process_info)

    def segundo_grau(self, numero_processo: str) -> None:
        process_info: ProcessInfo = {"Número do processo": numero_processo}
        process_info.update(self._informacoes_gerais_segundo_grau())
        process_info.update(self._info_processual_segundo_grau())

        self._partes_segundo_grau(numero_processo=numero_processo)
        self.to_add_processos_segundo_grau.append(process_info)

    def copia_pdf(
        self,
        data: dict[str, str | int | datetime],
    ) -> dict[str, str | int | datetime]:
        """Extract the movements of the legal proceedings and saves a PDF copy.

        Returns:
             dict[str, str | int | datetime]: Data return

        """
        id_proc = self.driver.find_element(
            By.CSS_SELECTOR,
            'input[name="id"]',
        ).get_attribute("value")

        btn_exportar = self.wait.until(
            ec.presence_of_element_located((
                By.CSS_SELECTOR,
                'input[id="btnMenuExportar"]',
            )),
        )
        time.sleep(0.5)
        btn_exportar.click()

        btn_exportar_processo = self.wait.until(
            ec.presence_of_element_located(
                (By.CSS_SELECTOR, 'input[id="exportarProcessoButton"]'),
            ),
        )
        time.sleep(0.5)
        btn_exportar_processo.click()

        def unmark_gen_mov() -> None:
            time.sleep(0.5)
            self.wait.until(
                ec.presence_of_element_located((
                    By.CSS_SELECTOR,
                    'input[name="gerarMovimentacoes"][value="false"]',
                )),
            ).click()

        def unmark_add_validate_tag() -> None:
            time.sleep(0.5)
            self.wait.until(
                ec.presence_of_element_located((
                    By.CSS_SELECTOR,
                    'input[name="adicionarTarjaValidacao"][value="false"]',
                )),
            ).click()

        def export() -> None:
            self.print_msg(
                message="Baixando cópia integral do processo...",
                type_log="log",
            )

            time.sleep(5)

            n_processo = self.bot_data.get("NUMERO_PROCESSO")
            path_pdf = Path(self.output_dir_path).joinpath(
                f"Cópia Integral - {n_processo} - {self.pid}.pdf",
            )

            btn_exportar = self.driver.find_element(
                By.CSS_SELECTOR,
                'input[name="btnExportar"]',
            )
            btn_exportar.click()

            count = 0
            time.sleep(5)
            path_copia = self.output_dir_path.joinpath(
                f"{id_proc}.pdf",
            ).resolve()

            while count <= 300:
                if path_copia.exists():
                    break

                time.sleep(2)
                count += 1

            if not path_copia.exists():
                raise ExecutionError(message="Arquivo não encontrado!")

            shutil.move(path_copia, path_pdf)

            time.sleep(0.5)
            data.update({"CÓPIA_INTEGRAL": path_pdf.name})

        unmark_gen_mov()
        unmark_add_validate_tag()
        export()

        return data
