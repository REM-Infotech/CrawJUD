"""Autenticador PJe."""

from __future__ import annotations

import traceback
from contextlib import suppress
from typing import TYPE_CHECKING
from uuid import uuid4

import jpype
import pyotp
import requests
from dotenv import dotenv_values

# Importa classes Java
from jpype import JClass
from selenium.common import TimeoutException
from selenium.common.exceptions import (
    UnexpectedAlertPresentException,
)
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from backend.common import auth_error
from backend.task_manager.constants import NO_CONTENT_STATUS
from backend.task_manager.constants.pje import ENDPOINT_DESAFIO
from backend.task_manager.resources.assinador import Assinador
from backend.task_manager.resources.auth.main import AutenticadorBot
from backend.task_manager.resources.elements import pje as el
from backend.task_manager.resources.formatadores import random_base36
from backend.task_manager.resources.keystore import KeyStore

if TYPE_CHECKING:
    from cryptography.x509 import Certificate

    from backend.task_manager.controllers.pje import PJeBot
    from backend.task_manager.resources.driver.web_element import WebElementBot

if not jpype.isJVMStarted():
    jpype.startJVM()

environ = dotenv_values()

ByteArrayInputStream = JClass("java.io.ByteArrayInputStream")
CertificateFactory = JClass("java.security.cert.CertificateFactory")
ArrayList = JClass("java.util.ArrayList")


class AutenticadorPJe(AutenticadorBot):
    """Implemente autenticação no PJe usando certificado digital.

    Atributos:
        _chain (list[Certificate]): Cadeia de certificados.
        bot (PJeBot): Instância do bot PJe.
    """

    _chain: list[Certificate]
    bot: PJeBot

    @property
    def regiao(self) -> str:
        """Retorne a região do bot PJe."""
        return str(self.bot.regiao)

    def __init__(self, bot: PJeBot) -> None:
        """Inicialize o autenticador PJe com certificado e chave.

        Args:
            bot (PJeBot): Instância do bot PJe.

        """
        super().__init__(bot=bot)

    def __call__(self) -> bool:
        """Realize o login no PJe e retorne True se for bem-sucedido.

        Returns:
            bool: Indica se o login foi realizado com sucesso.

        """
        sucesso_login = False
        try:
            url = el.LINK_AUTENTICACAO_SSO.format(regiao=self.regiao)
            self.driver.get(url)

            if "https://sso.cloud.pje.jus.br/" not in self.driver.current_url:
                return True

            self.wait.until(
                ec.presence_of_element_located((
                    By.CSS_SELECTOR,
                    el.CSS_FORM_LOGIN,
                )),
            )

            self._login_certificado()
            self._desafio_duplo_fator()
            sucesso_login = WebDriverWait(
                driver=self.driver,
                timeout=10,
                poll_frequency=0.3,
                ignored_exceptions=(UnexpectedAlertPresentException),
            ).until(ec.url_contains("pjekz"))

        except (
            TimeoutException,
            UnexpectedAlertPresentException,
            requests.RequestException,
        ) as e:
            exc = "\n".join(traceback.format_exception(e))
            self.print_message(
                message=f"Erro ao realizar autenticação: {exc}",
                message_type="error",
            )

        return sucesso_login

    def _login_certificado(self) -> None:
        # enviar diretamente ao endpoint PJe (exemplo)
        uuid_tarefa = str(uuid4())
        desafio = random_base36()
        assinador = Assinador(
            self.credenciais.certificado,
            self.credenciais.password,
        )
        conteudo_assinado = assinador.assinar_conteudo(desafio)

        base64_conteudo = conteudo_assinado.conteudo_assinado_base64
        cadeia_base64 = conteudo_assinado.cadeia_base64

        ssopayload = {
            "uuid": uuid_tarefa,
            "mensagem": desafio,
            "assinatura": base64_conteudo,
            "certChain": cadeia_base64,
        }

        resp = requests.post(ENDPOINT_DESAFIO, json=ssopayload, timeout=30)

        if resp.status_code != NO_CONTENT_STATUS:
            auth_error()

        self.driver.execute_script(el.COMMAND, el.ID_INPUT_DESAFIO, desafio)
        self.driver.execute_script(el.COMMAND, el.ID_CODIGO_PJE, uuid_tarefa)
        self.driver.execute_script("document.forms[0].submit()")

    def _desafio_duplo_fator(self) -> None:
        otp = str(pyotp.parse_uri(uri=self.credenciais.otp).now())

        input_otp: WebElementBot = WebDriverWait(self.driver, 60).until(
            ec.presence_of_element_located((
                By.CSS_SELECTOR,
                'input[id="otp"]',
            )),
        )

        input_otp.send_keys(otp)
        input_otp.send_keys(Keys.ENTER)

    def _confirmar_login(self) -> bool:
        with suppress(TimeoutException):
            return WebDriverWait(
                driver=self.driver,
                timeout=10,
                poll_frequency=0.3,
                ignored_exceptions=(UnexpectedAlertPresentException),
            ).until(ec.url_contains("pjekz"))

        return False

    def get_cookies(self) -> dict[str, str]:
        """Retorne os headers e cookies atuais do navegador."""
        return self._cookie_to_dict()

    def _cookie_to_dict(self) -> dict[str, str]:
        cookies_driver = self.driver.get_cookies()
        return {str(cookie["name"]): str(cookie["value"]) for cookie in cookies_driver}

    def _get_otp_uri(self) -> str:
        kp = KeyStore(self.credenciais.kdbx, self.credenciais.senha_kdbx)
        username = self.credenciais.cpf_cnpj_certificado
        entries = kp.find_entries({"username": username})

        if isinstance(entries, list):
            lista_filtrada = list(
                filter(
                    lambda x: x.otp and "sso.cloud.pje.jus.br" in x.url,
                    entries,
                ),
            )
            return lista_filtrada[-1].otp

        return entries.otp
