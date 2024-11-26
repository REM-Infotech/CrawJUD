import json
import os
import pathlib
import platform
import shutil
import ssl
import subprocess
import time
import unicodedata
from datetime import datetime
from typing import Dict, List, Union

import pandas as pd
import pytz
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from dotenv import load_dotenv
from openai import OpenAI
from pandas import Timestamp

# Selenium Imports
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from werkzeug.utils import secure_filename

from ...common.exceptions import ErroDeExecucao
from ...meta import classproperty
from ..Utils.Driver import GetDriver

TypeHint = Union[
    List[str],
    List[Dict[str, str | int | float | datetime]],
    Dict[str, str],
]


class CrawJUD:

    settings = {
        "recentDestinations": [{"id": "Save as PDF", "origin": "local", "account": ""}],
        "selectedDestinationId": "Save as PDF",
        "version": 2,
    }

    def __init__(self, **kwargs):

        self.__dict__.update(kwargs)
        self.kwrgs = kwargs
        self.setup()

    def __getattr__(self, nome: str) -> TypeHint:

        item = self.kwrgs.get(nome, None)

        if not item:
            item = CrawJUD.__dict__.get(nome, None)

            if not item:
                item = classproperty.kwrgs_.get(nome, None)

        return item

    """

    Esse umzilhão de property aqui é pra evitar a construção
    de um monte de classe toda vez que eu precisar dela.

    Com o property eu construo e deixo salvo estado dela

    """

    def client(self):

        load_dotenv()
        return OpenAI()

    def setup(self):

        try:
            with open(self.path_args, "rb") as f:
                json_f: dict[str, str | int] = json.load(f)

                self.kwrgs = json_f

                for key, value in json_f.items():
                    setattr(self, key, value)

            self.message = str("Inicializando robô")
            self.type_log = str("log")
            self.prt()

            self.output_dir_path = (
                pathlib.Path(self.path_args).parent.resolve().__str__()
            )
            # time.sleep(10)
            self.list_args = [
                "--ignore-ssl-errors=yes",
                "--ignore-certificate-errors",
                "--display=:99",
                "--window-size=1600,900",
                "--no-sandbox",
                "--disable-blink-features=AutomationControlled",
                "--kiosk-printing",
            ]
            self.system
            if self.name_cert:

                self.install_cert()

            time_xlsx = datetime.now(pytz.timezone("America/Manaus")).strftime(
                "%d-%m-%y"
            )

            namefile = f"Sucessos - PID {self.pid} {time_xlsx}.xlsx"
            self.path = f"{self.output_dir_path}/{namefile}"

            namefile_erro = f"Erros - PID {self.pid} {time_xlsx}.xlsx"
            self.path_erro = f"{self.output_dir_path}/{namefile_erro}"

            self.name_colunas = self.MakeXlsx("sucesso", self.typebot).make_output(
                self.path
            )
            self.MakeXlsx("erro", self.typebot).make_output(self.path_erro)

            if not self.xlsx:

                self.data_inicio = datetime.strptime(self.data_inicio, "%Y-%m-%d")
                self.data_fim = datetime.strptime(self.data_fim, "%Y-%m-%d")

            self.state_or_client = self.state if self.state is not None else self.client
            self.DriverLaunch()

        except Exception as e:

            self.row = 0
            self.message = "Falha ao iniciar. Informe a mensagem de erro ao suporte"
            self.type_log = "error"
            self.prt()
            self.message_error = str(e)
            self.prt()
            self.end_prt("Falha ao iniciar")
            raise e

    def auth_bot(self):

        if self.login_method:
            chk_logged = self.AuthBot.auth()
            if chk_logged is True:

                self.message = "Login efetuado com sucesso!"
                self.type_log = "log"
                self.prt()

            elif chk_logged is False:

                self.driver.quit()
                self.message = "Erro ao realizar login"
                self.type_log = "error"
                self.prt()
                raise Exception(self.message)

    def end_prt(self, status: str) -> None:

        print_bot = self.printtext()
        print_bot.end_bot(status)

    def prt(self) -> None:

        print_bot = self.printtext()
        print_bot.print_msg()

    def dataFrame(self) -> list[dict[str, str]]:

        input_file = os.path.join(
            pathlib.Path(self.path_args).parent.resolve().__str__(), str(self.xlsx)
        )

        df = pd.read_excel(input_file)
        df.columns = df.columns.str.upper()

        for col in df.columns.to_list():
            df[col] = df[col].apply(
                lambda x: (
                    x.strftime("%d/%m/%Y")
                    if type(x) is datetime or type(x) is Timestamp
                    else x
                )
            )

        for col in df.select_dtypes(include=["float"]).columns.to_list():
            df[col] = df[col].apply(lambda x: "{:.2f}".format(x).replace(".", ","))

        vars_df = []

        df_dicted = df.to_dict(orient="records")
        for item in df_dicted:
            for key, value in item.items():
                if str(value) == "nan":
                    item.update({key: None})

            vars_df.append(item)

        return vars_df

    def elawFormats(self, data: dict[str, str]) -> dict[str, str]:

        data_listed = list(data.items())
        for key, value in data_listed:

            if key.upper() == "TIPO_EMPRESA":
                data.update({"TIPO_PARTE_CONTRARIA": "Autor"})
                if value.upper() == "RÉU":
                    data.update({"TIPO_PARTE_CONTRARIA": "Autor"})

            elif key.upper() == "COMARCA":
                set_locale = self.cities_Amazonas().get(value, None)
                if not set_locale:
                    set_locale = "Outro Estado"

                data.update({"CAPITAL_INTERIOR": set_locale})

            elif key == "DATA_LIMITE" and not data.get("DATA_INICIO"):
                data.update({"DATA_INICIO": value})

            elif type(value) is int or type(value) is float:
                data.update({key: "{:.2f}".format(value).replace(".", ",")})

            elif key == "CNPJ_FAVORECIDO" and not value:
                data.update({key: "04.812.509/0001-90"})

        return data

    def calc_time(self) -> list:

        end_time = time.perf_counter()
        execution_time = end_time - self.start_time
        calc = execution_time / 60
        splitcalc = str(calc).split(".")
        minutes = int(splitcalc[0])
        seconds = int(float(f"0.{splitcalc[1]}") * 60)

        return [minutes, seconds]

    def append_moves(self) -> None:

        if len(self.appends) > 0:

            for append in self.appends:

                self.append_success(
                    append, "Movimentação salva na planilha com sucesso!!"
                )

        elif len(self.appends) == 0:
            raise ErroDeExecucao("Nenhuma Movimentação encontrada")

    def append_success(self, data, message=None, fileN: str = None):

        if not message:
            message = "Execução do processo efetuada com sucesso!"

        def save_info(data: list[dict[str, str]]):
            if not self.path:
                self.path = os.path.join(
                    pathlib.Path(self.path).parent.resolve(), fileN
                )

            if not os.path.exists(self.path):
                df = pd.DataFrame(data)
                df = df.to_dict(orient="records")

            elif os.path.exists(self.path):

                df = pd.read_excel(self.path)
                df = df.to_dict(orient="records")
                df.extend(data)

            new_data = pd.DataFrame(df)
            new_data.to_excel(self.path, index=False)

        typeD = type(data) is list and all(isinstance(item, dict) for item in data)

        if not typeD:

            data2 = {}

            for item in self.name_colunas:
                data2.update({item: ""})

            for item in data:
                for key, value in list(data2.items()):
                    if not value:
                        data2.update({key: item})
                        break

            data.clear()
            data.append(data2)

        save_info(data)

        if message:
            if self.type_log == "log":
                self.type_log = "success"

            self.message = message
            self.prt()

    def append_error(self, data: dict[str, str] = None):

        if not os.path.exists(self.path_erro):
            df = pd.DataFrame(data)
            df = df.to_dict(orient="records")

        elif os.path.exists(self.path_erro):
            df = pd.read_excel(self.path_erro)
            df = df.to_dict(orient="records")
            df.extend([data])

        new_data = pd.DataFrame(df)
        new_data.to_excel(self.path_erro, index=False)

    def format_String(self, string: str) -> str:

        return secure_filename(
            "".join(
                [
                    c
                    for c in unicodedata.normalize("NFKD", string)
                    if not unicodedata.combining(c)
                ]
            )
        )

    def finalize_execution(self) -> None:

        window_handles = self.driver.window_handles
        self.row = self.row + 1
        if len(window_handles) > 0:

            self.driver.delete_all_cookies()
            self.driver.close()

        end_time = time.perf_counter()
        execution_time = end_time - self.start_time
        calc = execution_time / 60
        minutes = int(calc)
        seconds = int((calc - minutes) * 60)

        self.end_prt("Finalizado")

        self.type_log = "success"
        self.message = f"Fim da execução, tempo: {minutes} minutos e {seconds} segundos"
        self.prt()

    def DriverLaunch(self) -> WebDriver:

        try:
            self.message = "Inicializando WebDriver"
            self.type_log = "log"
            self.prt()

            list_args = self.list_args

            chrome_options = Options()
            self.chr_dir = str(os.path.join(os.getcwd(), "Temp", self.pid, "chrome"))

            if os.getlogin() != "root" or platform.system() != "Linux":
                list_args.remove("--no-sandbox")

            if platform.system() == "Windows" and self.login_method == "cert":
                state = str(self.state)
                self.path_accepted = str(
                    os.path.join(os.getcwd(), "Browser", state, self.username, "chrome")
                )
                path_exist = os.path.exists(self.path_accepted)
                if path_exist:

                    for root, dirs, files in os.walk(self.path_accepted):
                        try:
                            shutil.copytree(root, self.chr_dir)
                        except Exception as e:
                            print(e)

                elif not path_exist:
                    os.makedirs(self.path_accepted, exist_ok=True)

            chrome_options.add_argument(f"user-data-dir={self.chr_dir}")
            for argument in list_args:
                chrome_options.add_argument(argument)

            this_path = pathlib.Path(__file__).parent.resolve().__str__()
            path_extensions = os.path.join(this_path, "extensions")
            for root, dirs, files in os.walk(path_extensions):
                for file_ in files:
                    if ".crx" in file_:
                        path_plugin = os.path.join(root, file_)
                        chrome_options.add_extension(path_plugin)

            chrome_prefs = {
                "download.prompt_for_download": False,
                "plugins.always_open_pdf_externally": True,
                "profile.default_content_settings.popups": 0,
                "printing.print_preview_sticky_settings.appState": json.dumps(
                    self.settings
                ),
                "download.default_directory": "{}".format(
                    os.path.join(self.output_dir_path)
                ),
            }

            chrome_options.add_experimental_option("prefs", chrome_prefs)
            pid_path = pathlib.Path(self.path_args).parent.resolve()
            getdriver = GetDriver(destination=pid_path)
            path_chrome = os.path.join(pid_path, getdriver())

            driver = webdriver.Chrome(
                service=Service(path_chrome), options=chrome_options
            )

            # driver.maximize_window()

            wait = WebDriverWait(driver, 20, 0.01)
            driver.delete_all_cookies()

            self.driver = driver
            self.wait = wait

            self.message = "WebDriver inicializado"
            self.type_log = "log"
            self.prt()

            return driver

        except Exception as e:
            raise e

    def install_cert(self) -> None:

        installed = self.is_pfx_certificate_installed(self.name_cert.split(".pfx")[0])

        if installed is False:

            path_cert = str(os.path.join(self.output_dir_path, self.name_cert))
            comando = [
                "certutil",
                "-importpfx",
                "-user",
                "-f",
                "-p",
                self.token,
                "-silent",
                path_cert,
            ]
            try:
                # Quando você passa uma lista, você geralmente não deve usar shell=True
                resultado = subprocess.run(
                    comando,
                    check=True,
                    text=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                )

                self.message = str(resultado.stdout)
                self.type_log = str("log")
                self.prt()

            except subprocess.CalledProcessError as e:
                raise e

    def is_pfx_certificate_installed(
        self, cert_subject_name: str, store_name: str = "MY"
    ):
        """
        Verifica se um certificado PFX específico está instalado no repositório 'MY'.

        Arguments:
            cert_subject_name (str): Nome do Assunto (Subject) do certificado para buscar.
            param store_name (str): Nome do repositório de certificados a ser verificado (default: "MY").

        :return: True se o certificado for encontrado, False caso contrário.
        """
        for cert, encoding, trust in ssl.enum_certificates(store_name):
            try:
                # Converte o certificado em formato DER para objeto X509
                x509_cert = x509.load_der_x509_certificate(cert, default_backend())

                # Obtém o nome do Assunto (Subject)
                subject_name = x509_cert.subject.rfc4514_string()

                # Verifica se o nome fornecido corresponde ao do certificado
                if cert_subject_name in subject_name:
                    return True
            except Exception as e:
                print(f"Erro ao processar o certificado: {e}")

        return False

    def group_date_all(self, data: dict[str, dict[str, str]]) -> list[dict[str, str]]:

        records = []
        for vara, dates in data.items():
            record = {}
            for date, entries in dates.items():
                for entry in entries:

                    record.update({"Data": date, "Vara": vara})
                    record.update(entry)
                    records.append(record)

        return records

    def group_keys(self, data: list[dict[str, str]]) -> dict[str, str]:

        record = {}
        for pos, entry in enumerate(data):
            for key, value in entry.items():

                if not record.get(key):
                    record.update({key: {}})

                record.get(key).update({str(pos): value})
        return record

    def Select2_ELAW(self, elementSelect: str, to_Search: str):

        selector: WebElement = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, elementSelect))
        )

        items = selector.find_elements(By.TAG_NAME, "option")
        opt_itens: dict[str, str] = {}

        elementsSelecting = elementSelect.replace("'", "'")
        if '"' in elementsSelecting:
            elementsSelecting = elementSelect.replace('"', "'")

        for item in items:

            value_item = item.get_attribute("value")
            cms = f"{elementsSelecting} > option[value='{value_item}']"
            text_item = self.driver.execute_script(f'return $("{cms}").text();')

            opt_itens.update({text_item.upper(): value_item})

        value_opt = opt_itens.get(to_Search.upper())

        if value_opt:

            command = f"$('{elementSelect}').val(['{value_opt}']);"
            command2 = f"$('{elementSelect}').trigger('change');"

            if "'" in elementSelect:
                command = f"$(\"{elementSelect}\").val(['{value_opt}']);"
                command2 = f"$(\"{elementSelect}\").trigger('change');"

            self.driver.execute_script(command)
            self.driver.execute_script(command2)

    def gpt_chat(self, text_mov: str) -> str:

        try:

            client = self.client()

            completion = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "Você é um assistente jurídico especializado em analisar processos judiciais. "
                            "Seu objetivo é identificar o tipo de documento (como petição inicial, contestação, "
                            "sentença, decisão interlocutória, etc.) e ajustar sua resposta com base no tipo do documento:"
                            "\n- Para sentenças e acórdãos: Extraia exclusivamente os valores mencionados no dispositivo "
                            "ou no conteúdo relacionado a condenações, como danos morais e materiais. Retorne apenas o valor e "
                            "o tipo do valor de forma resumida, no formato: 'Danos morais: R$ XXXX,XX; Danos materiais: R$ XXXX,XX; Inexigibilidade de débito: R$ XXXX,XX'."
                            "Nas Sentenças e acordãos, procure fazer diferenciação dos valores para evitar erros como entregar valores de limite de multa como danos morais ou qualquer "
                            "\n outro de forma errônea."
                            "\n- Para petições iniciais: Forneça um resumo do tema principal do processo com base na petição inicial e, em seguida, extraia os valores e os tipos de indenização solicitados pelo autor, como danos morais, materiais, lucros cessantes, inexigibilidade, ou outros pedidos monetários. "
                            "Resuma no formato: 'Tipo de documento: Petição Inicial; Assunto: [Resumo do tema do processo]; Danos morais: R$ XXXX,XX; Danos materiais: R$ XXXX,XX; Lucros cessantes: R$ XXXX,XX; Inexigibilidade: R$ XXXX,XX'."
                            "Caso não haja valores específicos, forneça apenas o resumo do tema principal do processo."
                            "\n- Para contestações: Forneça um resumo objetivo da linha de defesa apresentada."
                            "\n- Para decisões interlocutórias: Identifique claramente o tipo de decisão e extraia, de forma minimalista, "
                            "as obrigações ou designações impostas, como deferimento ou indeferimento de pedidos, determinações processuais, "
                            "ou outras medidas relevantes. Resuma no formato: 'Tipo de documento: Decisão interlocutória; Assunto: [Obrigações/designações principais]'."
                            "\n- Identifique claramente o tipo de documento no início da resposta."
                            "- Exemplo de comportamento esperado:\n"
                            "  - Entrada: 'Sentença: Condenou o réu a pagar R$ 10.000,00 de danos morais e R$ 5.000,00 de danos materiais.'\n"
                            "  - Saída: 'Danos morais: R$ 10.000,00; Danos materiais: R$ 5.000,00'\n"
                            "  - Entrada: 'Petição Inicial: O autor requer indenização por danos morais de R$ 50.000,00, danos materiais de R$ 30.000,00, e lucros cessantes de R$ 20.000,00, decorrentes de um acidente de trânsito.'\n"
                            "  - Saída: 'Tipo de documento: Petição Inicial; Assunto: Pedido de indenização por acidente de trânsito; Danos morais: R$ 50.000,00; Danos materiais: R$ 30.000,00; Lucros cessantes: R$ 20.000,00.'\n"
                            "  - Entrada: 'Petição Inicial: O autor solicita a declaração de inexigibilidade de débito no valor de R$ 15.000,00.'\n"
                            "  - Saída: 'Tipo de documento: Petição Inicial; Assunto: Pedido de declaração de inexigibilidade de débito; Inexigibilidade de débito: R$ 15.000,00.'\n"
                            "  - Entrada: 'Petição Inicial: O autor pleiteia indenização por danos morais e materiais decorrentes de erro médico.'\n"
                            "  - Saída: 'Tipo de documento: Petição Inicial; Assunto: Pedido de indenização por erro médico; Danos morais: Não especificado; Danos materiais: Não especificado.'\n"
                            "  - Entrada: 'Decisão interlocutória: O pedido de tutela foi deferido para reintegração de posse do imóvel.'\n"
                            "  - Saída: 'Tipo de documento: Decisão interlocutória; Assunto: Pedido de tutela deferido para reintegração de posse.'"
                        ),
                    },
                    {
                        "role": "user",
                        "content": (
                            f"Analise o seguinte texto e ajuste sua resposta de acordo com o tipo de documento: {text_mov}."
                        ),
                    },
                ],
                temperature=0.1,
                max_tokens=300,  # Ajuste conforme necessário
            )

            choices = completion.choices
            choice = choices[0]
            choice_message = choice.message
            text = choice_message.content

            if not text:
                text = text_mov

            return text
        except Exception as e:
            print(e)
            return text_mov

    @classproperty
    def system(self):
        return classproperty._system

    @system.setter
    def system(self, system_: str):
        classproperty._system = system_

    @classproperty
    def state_or_client(self):
        return classproperty._state_or_client_

    @state_or_client.setter
    def state_or_client(self, new_s: str):
        classproperty._state_or_client_ = new_s

    @classproperty
    def type_log(self):
        return classproperty._type_log

    @type_log.setter
    def type_log(self, new_log: str):
        classproperty._type_log = new_log

    @classproperty
    def pid(self) -> int:
        return classproperty._pid

    @pid.setter
    def pid(self, pid_) -> int:
        classproperty._pid = pid_

    @classproperty
    def message(self) -> str:
        return classproperty._message

    @message.setter
    def message(self, new_msg: str) -> str:
        classproperty._message = new_msg

    @classproperty
    def isStoped(self):
        chk = os.path.exists(os.path.join(self.output_dir_path, f"{self.pid}.flag"))
        return chk

    @classproperty
    def driver(self) -> WebDriver:
        return classproperty.drv

    @driver.setter
    def driver(self, new_drv: WebDriver):
        classproperty.drv = new_drv

    @classproperty
    def wait(self) -> WebDriverWait:
        return classproperty.wt

    @wait.setter
    def wait(self, new_wt: WebDriverWait):
        classproperty.wt = new_wt

    @classproperty
    def chr_dir(self):
        return classproperty.user_data_dir

    @chr_dir.setter
    def chr_dir(self, new_dir: str):
        classproperty.user_data_dir = new_dir

    @classproperty
    def output_dir_path(self):
        return classproperty.out_dir

    @output_dir_path.setter
    def output_dir_path(self, new_outdir: str):
        classproperty.out_dir = new_outdir

    @classproperty
    def kwrgs(self) -> dict:
        return classproperty.kwrgs_

    @kwrgs.setter
    def kwrgs(self, new_kwg):
        classproperty.kwrgs_ = new_kwg

    @classproperty
    def row(self) -> int:
        return classproperty.row_

    @row.setter
    def row(self, new_row: int):
        classproperty.row_ = new_row

    @classproperty
    def message_error(self) -> str:
        return classproperty.message_error_

    @message_error.setter
    def message_error(self, nw_m: str) -> str:
        classproperty.message_error_ = nw_m

    @classproperty
    def graphicMode(self):
        return classproperty.graphicMode_

    @graphicMode.setter
    def graphicMode(self, new_graph):
        classproperty.graphicMode_ = new_graph

    @classproperty
    def list_args(self):
        return [
            "--ignore-ssl-errors=yes",
            "--ignore-certificate-errors",
            "--display=:99",
            "--window-size=1600,900",
            "--no-sandbox",
            "--disable-blink-features=AutomationControlled",
            "--kiosk-printing",
        ]

    @list_args.setter
    def list_args(self, new_Args: list[str]):
        classproperty.cr_list_args = new_Args

    @classproperty
    def bot_data(self) -> dict:
        return classproperty.bot_data_

    @bot_data.setter
    def bot_data(self, new_botdata: dict):
        classproperty.bot_data_ = new_botdata

    @classproperty
    def AuthBot(self):
        from ..Utils.auth import AuthBot

        return AuthBot()

    @classproperty
    def SearchBot(self):

        from ..Utils.search import SeachBot

        return SeachBot()

    @classproperty
    def interact(self):
        from ..Utils.interator import Interact

        return Interact()

    @classproperty
    def printtext(self):
        from ..Utils.PrintLogs import printbot

        return printbot

    @classproperty
    def MakeXlsx(self):
        from ..Utils.MakeTemplate import MakeXlsx

        return MakeXlsx

    @classproperty
    def cities_Amazonas(self):
        from ..Utils.dicionarios import cities_Amazonas

        return cities_Amazonas

    @classproperty
    def elements(self):
        from ..Utils.elements import ElementsBot

        return ElementsBot().Elements

    @classproperty
    def vara(self) -> str:
        return classproperty.vara_

    @vara.setter
    def vara(self, vara_str: str):
        classproperty.vara_ = vara_str

    @classproperty
    def path_accepted(self):
        return classproperty.path_accepted_

    @path_accepted.setter
    def path_accepted(self, new_path: str):
        classproperty.path_accepted_ = new_path
