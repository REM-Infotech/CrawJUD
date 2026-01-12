# ruff: noqa: BLE001

"""Extração de informações de processos no Projudi.

Este pacote contém classes e funções para automatizar a
coleta de dados processuais do sistema Projudi.
"""

from __future__ import annotations

from contextlib import suppress
from shutil import move
from time import sleep
from typing import TYPE_CHECKING, ClassVar, TypedDict

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec

from backend.common import raise_execution_error
from backend.common.exceptions import ExecutionError
from backend.dicionarios import ArgumentosRobo, ProjudiCapa

from ._primeira import PrimeiraInstancia
from ._segunda import SegundaInstancia

if TYPE_CHECKING:
    from datetime import datetime

    from backend.dicionarios import (
        PartesProjudiDict as PartesProjudi,
    )
    from backend.dicionarios import (
        RepresentantesProjudiDict as RepresentantesProjudi,
    )
CONTAGEM = 300


class InformacaoExtraida(TypedDict):
    PrimeiraInstancia: list[ProjudiCapa]
    SegundaInstancia: list[ProjudiCapa]
    Partes: list[PartesProjudi]
    Advogados: list[RepresentantesProjudi]


class Capa(PrimeiraInstancia, SegundaInstancia):
    """Implemente automação para extrair dados do Projudi.

    Esta classe reúne métodos para coletar informações
    processuais de diferentes instâncias do sistema Projudi.
    """

    name: ClassVar[str] = "capa_projudi"
    frame: list[ProjudiCapa]
    informacao_extraida: InformacaoExtraida

    def run(self, config: ArgumentosRobo) -> None:

        config.update({
            "sistema": "projudi",
        })
        if config.get("frame"):
            self.frame = config.get("frame")

        self.args = config
        self.setup(config)
        return self.execution()

    def execution(self) -> InformacaoExtraida:
        """Execute a extração de dados dos processos do Projudi."""
        self.informacao_extraida = {
            "PrimeiraInstancia": [],
            "SegundaInstancia": [],
            "Partes": [],
            "Advogados": [],
        }
        for pos, value in enumerate(self.frame):
            if self.bot_stopped.is_set():
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

                self.print_message(
                    message=f"{message_error}.",
                    message_type="error",
                )

                self.bot_data.update({"MOTIVO_ERRO": message_error})
                self.append_error(data_save=[self.bot_data])

        self.finalizar_execucao()
        return self.informacao_extraida

    def queue(self) -> None:

        try:
            driver = self.driver
            bot_data = self.bot_data

            search = self.search()
            trazer_copia = bot_data.get("TRAZER_COPIA", "não")
            if not search:
                return

            self.print_message(
                message="Extraindo informações...",
                message_type="info",
            )

            driver.refresh()
            self.get_process_informations()

            if trazer_copia and trazer_copia.lower() == "sim":
                self.copia_pdf()

            self.print_message(
                message="Informações extraídas com sucesso!",
                message_type="success",
            )
        except Exception as e:
            msg = "Erro ao buscar processo!"
            raise ExecutionError(message=msg, exc=e) from e

    def get_process_informations(self) -> None:
        """Extrai informações detalhadas do processo da página atual do Projudi."""
        try:
            bot_data = self.bot_data
            numero_processo = bot_data.get("NUMERO_PROCESSO")

            callables = {
                "1": self.primeiro_grau,
                "2": self.segundo_grau,
            }

            callables[str(bot_data.get("GRAU", "1"))](
                numero_processo=numero_processo,
            )

        except ExecutionError, Exception:
            raise_execution_error("Erro ao executar operação")

    def primeiro_grau(self, numero_processo: str) -> None:
        process_info = ProjudiCapa(NUMERO_PROCESSO=numero_processo)

        list_items = dir(ProjudiCapa)
        for item in list_items:
            val = process_info.get(item)
            if not val and not item.startswith("_") and not callable(getattr(ProjudiCapa, item)):
                process_info.update({item: "Vazio"})

        informacoes_gerais = self._informacoes_gerais_primeiro_grau()
        informacao_processo = self._info_processual_primeiro_grau()

        process_info.update(informacoes_gerais)
        process_info.update(informacao_processo)

        partes, advogados = self._partes_primeiro_grau(
            numero_processo=numero_processo,
        )

        to_add = InformacaoExtraida(
            PrimeiraInstancia=[process_info],
            Partes=partes,
            Advogados=advogados,
        )

        self.informacao_extraida["PrimeiraInstancia"].append(process_info)
        self.informacao_extraida["Partes"].extend(partes)
        self.informacao_extraida["Advogados"].extend(advogados)

        for key, value in list(to_add.items()):
            self.append_success(worksheet=key, data_save=value)

    def segundo_grau(self, numero_processo: str) -> None:
        process_info = ProjudiCapa(NUMERO_PROCESSO=numero_processo)

        list_items = dir(ProjudiCapa)
        for item in list_items:
            val = process_info.get(item)
            if not val and not item.startswith("_") and not callable(getattr(ProjudiCapa, item)):
                process_info.update({item: "Vazio"})

        informacoes_gerais = self._informacoes_gerais_segundo_grau()
        informacao_processo = self._info_processual_segundo_grau()

        process_info.update(informacoes_gerais)
        process_info.update(informacao_processo)

        partes, advogados = self._partes_segundo_grau(
            numero_processo=numero_processo,
        )

        to_add = InformacaoExtraida(
            SegundaInstancia=[process_info],
            Partes=partes,
            Advogados=advogados,
        )

        self.informacao_extraida["SegundaInstancia"].append(process_info)
        self.informacao_extraida["Partes"].extend(partes)
        self.informacao_extraida["Advogados"].extend(advogados)

        for key, value in list(to_add.items()):
            self.append_success(worksheet=key, data_save=value)

    def copia_pdf(self) -> dict[str, str | int | datetime]:
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
        sleep(0.5)
        btn_exportar.click()

        btn_exportar_processo = self.wait.until(
            ec.presence_of_element_located(
                (By.CSS_SELECTOR, 'input[id="exportarProcessoButton"]'),
            ),
        )
        sleep(0.5)
        btn_exportar_processo.click()

        self.unmark_gen_mov()
        self.unmark_add_validate_tag()
        self.export(id_proc)

    def unmark_gen_mov(self) -> None:
        sleep(0.5)
        self.wait.until(
            ec.presence_of_element_located((
                By.CSS_SELECTOR,
                'input[name="gerarMovimentacoes"][value="false"]',
            )),
        ).click()

    def unmark_add_validate_tag(self) -> None:
        sleep(0.5)
        self.wait.until(
            ec.presence_of_element_located((
                By.CSS_SELECTOR,
                'input[name="adicionarTarjaValidacao"][value="false"]',
            )),
        ).click()

    def export(self, id_proc: str) -> None:
        self.print_message(
            message="Baixando cópia integral do processo...",
            message_type="log",
        )

        sleep(5)
        n_processo = self.bot_data.get("NUMERO_PROCESSO")

        out_dir = self.output_dir_path
        nome_pdf = f"2026 - COPIA INTEGRAL - {n_processo} - {self.id_execucao}.pdf"
        path_pdf = out_dir.joinpath(n_processo, nome_pdf)
        path_pdf.parent.mkdir(exist_ok=True, parents=True)

        btn_exportar = self.driver.find_element(
            By.CSS_SELECTOR,
            'input[name="btnExportar"]',
        )
        btn_exportar.click()

        count = 0
        sleep(5)
        path_copia = out_dir.joinpath(f"{id_proc}.pdf").resolve()

        while count <= CONTAGEM:
            if path_copia.exists():
                break

            sleep(2)
            count += 1

        if not path_copia.exists():
            raise ExecutionError(message="Arquivo não encontrado!")

        move(path_copia, path_pdf)
        sleep(2.5)
