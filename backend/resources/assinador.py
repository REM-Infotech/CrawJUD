"""Autenticador PJe."""

from __future__ import annotations

import base64
from pathlib import Path
from typing import TYPE_CHECKING, ClassVar, cast

import jpype
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import (
    Encoding,
)
from cryptography.hazmat.primitives.serialization.pkcs12 import (
    PKCS12Certificate,
    PKCS12KeyAndCertificates,
    load_pkcs12,
)
from dotenv import dotenv_values

# Importa classes Java
from jpype import JArray, JByte

if TYPE_CHECKING:
    from cryptography.x509 import Certificate

    from backend.controllers.pje import PJeBot
    from typings import Algoritmos, PrivateKey

if not jpype.isJVMStarted():
    jpype.startJVM()

    from jpype import imports as imports

from java.io import ByteArrayInputStream
from java.security.cert import CertificateFactory
from java.util import ArrayList

environ = dotenv_values()


class ConteudoAssinado:
    """Classe que representa um conteúdo assinado e sua cadeia de certificados.

    Attributes
    ----------
    _chain : list[PKCS12Certificate]
        Cadeia de certificados utilizada na assinatura.
    _conteudo_assinado : bytes
        Conteúdo assinado em formato binário.

    """

    _chain: list[PKCS12Certificate]
    _conteudo_assinado: bytes

    def __init__(
        self,
        conteudo_assinado: bytes,
        certificado: PKCS12Certificate,
        cadeia: list[PKCS12Certificate],
    ) -> None:
        """Inicializa o ConteudoAssinado.

        Parameters
        ----------
        conteudo_assinado : bytes
            Conteúdo assinado em formato binário.
        certificado : PKCS12Certificate
            Certificado utilizado na assinatura.
        cadeia : list[PKCS12Certificate]
            Cadeia de certificados utilizada na assinatura.

        """
        self._chain = cadeia
        self._cert = certificado
        self._conteudo_assinado = conteudo_assinado

    @property
    def conteudo_assinado_base64(self) -> str:
        return base64.b64encode(self._conteudo_assinado).decode()

    @property
    def cadeia_base64(self) -> str:
        cf = CertificateFactory.getInstance("X.509")
        java_chain = ArrayList()

        for cert in self._chain:
            # converte o certificado DER em InputStream Java
            der = cert.public_bytes(Encoding.DER)
            der_array = JArray(JByte)(der)
            bais = ByteArrayInputStream(der_array)
            java_cert = cf.generateCertificate(bais)
            java_chain.add(java_cert)

        # gera o CertPath e exporta em formato PkiPath
        cert_path = cf.generateCertPath(java_chain)
        pkipath_bytes = cert_path.getEncoded("PkiPath")

        return base64.b64encode(bytes(pkipath_bytes)).decode("utf-8")


class Assinador:
    """Classe responsável por assinar conteúdos utilizando certificados digitais."""

    _chain: list[Certificate]
    bot: PJeBot
    _certificado_carregado: PKCS12KeyAndCertificates = None
    algoritmos_suportados: ClassVar[dict[Algoritmos, hashes.HashAlgorithm]] = {
        "SHA256withRSA": hashes.SHA256(),
        "SHA1withRSA": hashes.SHA1(),
        "MD5withRSA": hashes.MD5(),
    }

    def __init__(
        self,
        certificado: str | None = None,
        senha_certificado: str | None = None,
    ) -> None:
        """Inicialize o objeto Assinador com o certificado digital e senha.

        Args:
            certificado (str | None): Caminho para o certificado digital.
            senha_certificado (str | None): Senha do certificado digital.

        """
        senha_certificado = senha_certificado.encode()
        certificado = Path(certificado).read_bytes()
        self.certificado_carregado = load_pkcs12(certificado, senha_certificado)

    def assinar_conteudo(
        self,
        conteudo: str | bytes,
        algoritmo_assinatura: Algoritmos = "MD5withRSA",
    ) -> ConteudoAssinado:
        if isinstance(conteudo, str):
            conteudo = conteudo.encode()

        algoritmo = self.algoritmos_suportados.get(algoritmo_assinatura)
        if not algoritmo:
            raise ValueError("Algoritmo não suportado: " + algoritmo_assinatura)

        pad = padding.PKCS1v15()
        conteudo_assinado = cast(
            "bytes",
            self.chave.sign(conteudo, pad, algoritmo),
        )

        return ConteudoAssinado(
            conteudo_assinado=conteudo_assinado,
            certificado=self.certficado,
            cadeia=self.cadeia,
        )

    @property
    def certificado_carregado(self) -> PKCS12KeyAndCertificates:
        return self._certificado_carregado

    @certificado_carregado.setter
    def certificado_carregado(self, valor: PKCS12KeyAndCertificates) -> None:
        self._certificado_carregado = valor

    @property
    def chave(self) -> PrivateKey:
        return self.certificado_carregado.key

    @property
    def certficado(self) -> PKCS12Certificate | None:
        return self.certificado_carregado.cert.certificate

    @property
    def cadeia(self) -> list[PKCS12Certificate]:
        chain = [self.certficado]
        chain.extend(
            [cert.certificate for cert in self.certificado_carregado.additional_certs],
        )
        return chain
