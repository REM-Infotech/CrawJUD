"""Gerencia operações com certificados digitais no Windows.

Inclui funções para instalar e remover certificados PFX via PowerShell.
"""

from __future__ import annotations

import subprocess
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from backend.task_manager.types_app import AnyType


class CertManagerError(Exception):
    """Lança erro personalizado para operações de certificado."""

    def __init__(  # noqa: D107
        self,
        mensagem: str,
        *args: AnyType,
        **kwargs: AnyType,
    ) -> None:
        self.__str__ = lambda: mensagem
        super().__init__(*args, **kwargs)


class CertManager:
    """Gerencie certificados digitais no Windows via PowerShell."""

    thumbprint: str = None

    @classmethod
    def _run_ps(cls, script: str) -> str:
        """Execute comando PowerShell e retorne saída padrão.

        Args:
            script (str): Script PowerShell a ser executado.

        Returns:
            str: Saída padrão do comando PowerShell.

        Raises:
            CertManagerError: Se o comando retornar erro.

        """
        # Monta o comando PowerShell para execução
        cmd: list[str] = [
            "powershell",
            "-NoLogo",
            "-NoProfile",
            "-NonInteractive",
            "-Command",
            script,
        ]

        # Executa o comando e captura a saída
        result = subprocess.run(
            cmd,
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )

        # Verifica se houve erro na execução
        if result.returncode != 0:
            raise CertManagerError(
                mensagem=f"PowerShell error: {result.stderr.strip()}",
            ) from None

        # Retorna a saída padrão do comando
        return result.stdout.strip()

    @classmethod
    def install_pfx(cls, pfx_path: str, pfx_password: str) -> str:
        r"""Instale certificado PFX no repositório CurrentUser\My.

        Args:
            pfx_path (str): Caminho do arquivo PFX.
            pfx_password (str): Senha do certificado.

        Returns:
            str: Thumbprint do certificado instalado.

        """
        # Monta o script PowerShell para importar o certificado
        script = f"""
        $pwd = ConvertTo-SecureString -String '{pfx_password}' -AsPlainText -Force;
        $cert = Import-PfxCertificate -FilePath '{pfx_path}' -Password $pwd -CertStoreLocation 'Cert:\\CurrentUser\\My';
        $cert.Thumbprint
        """

        # Executa o script e armazena o thumbprint
        output: str = CertManager._run_ps(script)
        cls.thumbprint = output
        return output

    @classmethod
    def uninstall_pfx(cls) -> bool:
        """Remova certificado pelo thumbprint e retorne status booleano.

        Returns:
            bool: True se removido, False se não encontrado.

        """
        # Monta o script PowerShell para remover o certificado pelo thumbprint
        script = f"""
        $path = 'Cert:\\CurrentUser\\My\\{cls.thumbprint}';
        if (Test-Path $path) {{
            Remove-Item -Path $path -Force;
            'Removed';
        }} else {{
            'NotFound';
        }}
        """

        # Executa o script e verifica se o certificado foi removido
        output: str = CertManager._run_ps(script)
        return output == "Removed"
