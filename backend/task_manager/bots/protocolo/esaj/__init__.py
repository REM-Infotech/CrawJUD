"""Gerencie operações de protocolo no sistema ESaj via CrawJUD.

Este pacote contém classes e funções para automação do
peticionamento eletrônico no ESaj.
"""

from __future__ import annotations

import shutil
import unicodedata
from contextlib import suppress
from pathlib import Path
from time import sleep
from typing import TYPE_CHECKING

from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
)
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from backend.common.exceptions import ExecutionError
from backend.common.raises import raise_execution_error
from backend.resources.elements import esaj as el
from backend.task_manager.controllers.esaj import ESajBot

if TYPE_CHECKING:
    from backend.resources.driver import WebElementBot


class Protocolo(ESajBot):
    """Class Protocolo.

    Manage protocol operations in the ESaj system via CrawJUD.

    Attributes:
        start_time (float): Time when the protocol process starts.
        bot_data (dict): Data for the current protocol entry.


    Methods:
        initialize: Create and return a new Protocolo instance.
        execution: Run protocol processing loop.
        queue: Execute protocoling steps with error handling.
        init_protocolo: Start the petition process.
        set_tipo_protocolo: Select and input the protocol type.
        set_subtipo_protocolo: Select and input the protocol subtype.
        set_petition_file: Attach the petition document.
        vincular_parte: Link a party to the petition.
        finish_petition: Finalize petition process.
        get_confirm_protocol: Confirm protocol and process receipt.

    """

    def execution(self) -> None:
        """Execute protocol processing on each row.

        Iterates over protocol rows and handles session renewals and errors.

        """
        frame = self.frame
        self.total_rows = len(frame)

        for pos, value in enumerate(frame):
            self.row = pos + 1
            self.bot_data = value

            with suppress(Exception):
                if self.driver.title.lower() == "a sessao expirou":
                    self.auth()

            try:
                self.queue()

            except ExecutionError as e:
                message_error = str(e)

                self.print_message(
                    message=f"{message_error}.",
                    message_type="error",
                )

                self.bot_data.update({"MOTIVO_ERRO": message_error})
                self.append_error(data_save=[self.bot_data])

        self.finalizar_execucao()

    def queue(self) -> None:
        """Execute etapas do protocolo com tratamento de erros.

        Raises:
            ExecutionError: Caso ocorra erro em alguma etapa.

        """
        try:
            self.search()
            self.init_protocolo()
            self.set_tipo_protocolo()
            self.set_subtipo_protocolo()
            self.set_petition_file()
            self.vincular_parte()
            self.finish_petition()
            data = self.get_confirm_protocol()
            self.append_success(data, message=data[1])

        except ExecutionError as e:
            raise ExecutionError(exc=e) from e

    def init_protocolo(self) -> None:
        """Inicie o peticionamento no sistema ESaj.

        Raises:
            ExecutionError: Caso ocorra erro ao inicializar peticionamento.

        """
        try:
            try:
                self.prt.print_log(
                    "log",
                    "Processo encontrado! Inicializando peticionamento...",
                )
                button_peticionamento = WebDriverWait(
                    self.driver,
                    10,
                ).until(
                    ec.element_to_be_clickable((By.ID, "pbPeticionar")),
                )
                link = button_peticionamento.get_attribute(
                    "onclick",
                ).split(
                    "'",
                )[1]
                self.driver.execute_script(
                    f"return window.location.href = '{link}';",
                )
                sleep(5)

            except TimeoutException:
                button_enterproc = WebDriverWait(self.driver, 5).until(
                    ec.presence_of_element_located((
                        By.CSS_SELECTOR,
                        "#processoSelecionado",
                    )),
                )
                button_enterproc.click()

                enterproc = WebDriverWait(self.driver, 5).until(
                    ec.element_to_be_clickable((
                        By.CSS_SELECTOR,
                        "#botaoEnviarIncidente",
                    )),
                )
                enterproc.click()
                button_peticionamento = WebDriverWait(
                    self.driver,
                    10,
                ).until(
                    ec.element_to_be_clickable((By.ID, "pbPeticionar")),
                )
                link = button_peticionamento.get_attribute(
                    "onclick",
                ).split(
                    "'",
                )[1]
                self.driver.execute_script(
                    f"return window.location.href = '{link}';",
                )

        except Exception as e:
            raise ExecutionError(
                message="Erro ao inicializar peticionamento",
                exc=e,
            ) from e

    def set_tipo_protocolo(self) -> None:
        """Informe o tipo de protocolo no sistema ESaj.

        Raises:
            ExecutionError: Caso ocorra erro ao informar o tipo.

        """
        try:
            self.sleep_load('div[id="loadFeedback"]')
            self.prt.print_log(
                "log",
                "Informando tipo de peticionamento",
            )
            button_classification = self.wait.until(
                ec.presence_of_element_located((
                    By.ID,
                    el.editar_classificacao,
                )),
            )
            self.interact.click(button_classification)

            select_tipo_peticao = self.wait.until(
                ec.presence_of_element_located((
                    By.CSS_SELECTOR,
                    el.selecionar_classe,
                )),
            )
            select_tipo_peticao = select_tipo_peticao.find_element(
                By.CSS_SELECTOR,
                el.toggle,
            )
            self.interact.click(select_tipo_peticao)

            input_tipo_peticao = self.wait.until(
                ec.presence_of_element_located((
                    By.CSS_SELECTOR,
                    el.input_classe,
                )),
            )
            self.interact.send_keys(
                input_tipo_peticao,
                self.bot_data.get("TIPO_PROTOCOLO"),
            )
            sleep(1.5)
            self.interact.send_keys(input_tipo_peticao, Keys.ENTER)

        except Exception as e:
            raise ExecutionError(
                message="Erro ao informar tipo de protocolo",
                exc=e,
            ) from e

    def set_subtipo_protocolo(self) -> None:
        """Informe o subtipo de protocolo no sistema ESaj.

        Raises:
            ExecutionError: Caso ocorra erro ao informar o subtipo.

        """
        try:
            self.prt.print_log(
                "log",
                "Informando subtipo de peticionamento",
            )
            select_categoria_peticao = self.wait.until(
                ec.presence_of_element_located((
                    By.CSS_SELECTOR,
                    el.select_categoria,
                )),
            )
            select_categoria_peticao = select_categoria_peticao.find_element(
                By.CSS_SELECTOR,
                el.toggle,
            )
            self.interact.click(select_categoria_peticao)

            input_categoria_peticao = self.wait.until(
                ec.presence_of_element_located((
                    By.CSS_SELECTOR,
                    el.input_categoria,
                )),
            )
            self.interact.send_keys(
                input_categoria_peticao,
                self.bot_data.get("SUBTIPO_PROTOCOLO"),
            )

            input_categoria_peticao_option = self.wait.until(
                ec.presence_of_element_located((
                    By.XPATH,
                    el.selecionar_grupo,
                )),
            )
            input_categoria_peticao_option.click()
            sleep(1)

        except Exception as e:
            raise ExecutionError(
                message="Erro ao informar subtipo de protocolo",
                exc=e,
            ) from e

    def set_petition_file(self) -> None:
        """Attach petition file.

        Uploads the petition document and verifies its successful submission.

        Raises:
            ExecutionError: If the petition file fails to upload.

        """
        try:
            self.prt.print_log("log", "Anexando petição")
            input_file = self.wait.until(
                ec.presence_of_element_located((
                    By.CSS_SELECTOR,
                    el.input_documento,
                )),
            )
            sleep(2)

            path_file = Path(self.path_args).parent.resolve()
            file = str(
                path_file.joinpath(
                    self.bot_data.get("PETICAO_PRINCIPAL"),
                ),
            )

            file = file.replace(" ", "")
            if "_" in file:
                file = file.replace("_", "")

            file = unicodedata.normalize("NFKD", file)
            file = "".join([c for c in file if not unicodedata.combining(c)])

            input_file.send_keys(file)

            file_uploaded = ""
            with suppress(TimeoutException):
                file_uploaded = WebDriverWait(self.driver, 25).until(
                    ec.presence_of_element_located((
                        By.XPATH,
                        el.documento,
                    )),
                )

            if not file_uploaded:
                raise_execution_error(message="Erro ao enviar petição")

            self.prt.print_log(
                "log",
                "Petição do processo anexada com sucesso",
            )

        except Exception as e:
            raise ExecutionError(
                message="Erro ao enviar petição",
                exc=e,
            ) from e

    def vincular_parte(self) -> None:
        """Vincule a parte à petição conforme os dados do bot.

        Raises:
            ExecutionError: Caso não seja possível vincular a parte.

        """
        try:
            parte_peticao = str(self.bot_data.get("PARTE_PETICIONANTE")).lower()
            self.prt.print_log("log", "Vinculando parte a petição...")
            partes = self.wait.until(
                ec.presence_of_all_elements_located((
                    By.CSS_SELECTOR,
                    el.processo_view,
                )),
            )
            if partes:
                self._vincular_parte_peticao(partes, parte_peticao)
            else:
                raise_execution_error(
                    message="Não foi possivel vincular parte a petição",
                )

        except Exception as e:
            raise ExecutionError(
                message="Não foi possivel vincular parte a petição",
                exc=e,
            ) from e

    def _vincular_parte_peticao(
        self,
        partes: list[WebElementBot],
        parte_peticao: str,
    ) -> None:
        """Auxilia na vinculação da parte à petição.

        Args:
            partes (list): Lista de elementos de partes.
            parte_peticao (str): Nome da parte a ser vinculada.

        """
        for parte_elem in partes:
            parte_name = parte_elem.find_element(
                By.CSS_SELECTOR,
                el.nome,
            ).text.lower()
            if parte_name == parte_peticao:
                sleep(3)

                incluir_button = None
                with suppress(NoSuchElementException):
                    incluir_button = parte_elem.find_element(
                        By.CSS_SELECTOR,
                        el.botao_incluir_peticao,
                    )

                if not incluir_button:
                    with suppress(NoSuchElementException):
                        incluir_button = parte_elem.find_element(
                            By.CSS_SELECTOR,
                            el.botao_incluir_partecontraria,
                        )

                incluir_button.click()

                self.prt.print_log(
                    "log",
                    "Vinculando cliente à petição...",
                )
                sleep(0.3)
                break

            if parte_name != parte_peticao:
                partes_view = self.driver.find_elements(
                    By.CSS_SELECTOR,
                    el.parte_view,
                )
                for parte_view_elem in partes_view:
                    parte_view_name = parte_view_elem.find_element(
                        By.CSS_SELECTOR,
                        el.nome,
                    ).text.lower()
                    if parte_view_name == parte_peticao.lower():
                        self.prt.print_log(
                            "log",
                            "Parte já vinculada, finalizando peticionamento...",
                        )
                        sleep(0.3)
                        break

    def finish_petition(self) -> None:
        """Finalize petition process.

        Completes the petition process by confirming and saving process details.

        # Inline: Click finish and then confirm the petition.
        """
        self.prt.print_log("log", "Finalizando...")

        finish_button = self.driver.find_element(
            By.XPATH,
            el.botao_protocolar,
        )
        sleep(1)
        finish_button.click()
        sleep(5)

        confirm_button = self.wait.until(
            ec.presence_of_element_located((
                By.CSS_SELECTOR,
                el.botao_confirmar,
            )),
        )
        confirm_button.click()

    def get_confirm_protocol(self) -> list:
        """Confirma protocolo e obtenha informações do recibo.

        Returns:
            list: Lista com número do processo, mensagem e nome do recibo.

        Raises:
            ExecutionError: Caso ocorra erro ao confirmar protocolo.

        """
        try:
            getlinkrecibo = WebDriverWait(self.driver, 60).until(
                ec.presence_of_element_located((
                    By.CSS_SELECTOR,
                    el.botao_recibo,
                )),
            )

            sleep(3)

            processo = self.bot_data.get("NUMERO_PROCESSO")
            name_recibo = f"Recibo Protocolo - {processo} - PID {self.pid}.pdf"
            self.driver.get_screenshot_as_file(
                f"{self.output_dir_path}/{name_recibo.replace('.pdf', '.png')}",
            )

            getlinkrecibo.click()

            path = Path(self.output_dir_path).joinpath(name_recibo)
            pathpdf = Path(self.path_args).parent.joinpath(
                "recibo.pdf",
            )

            while True:
                if pathpdf.exists(pathpdf):
                    sleep(0.5)
                    break

            shutil.move(pathpdf, path)
            return [
                self.bot_data.get("NUMERO_PROCESSO"),
                f"Processo nº{processo} protocolado com sucesso!",
                name_recibo,
            ]

        except ExecutionError as e:
            raise ExecutionError(
                message="Erro ao confirmar protocolo",
                e=e,
            ) from e
