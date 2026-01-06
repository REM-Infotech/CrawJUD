"""Implemente buscas de processos no sistema PJe.

Este módulo contém classes e funções para consultar processos
no sistema PJe utilizando um cliente HTTP.
"""

from __future__ import annotations

from contextlib import suppress
from json.decoder import JSONDecodeError
from typing import TYPE_CHECKING, TypedDict

from backend.interfaces.pje import DictResults
from backend.resources.elements import pje as el
from backend.resources.search.main import SearchBot
from backend.task_manager.constants import HTTP_OK_STATUS

if TYPE_CHECKING:
    from httpx import Client, Response

    from backend.controllers import PJeBot
    from backend.interfaces import BotData


class _ResponseDadosBasicos(TypedDict):
    id: int
    numeroIdentificacaoJustica: int
    numero: str
    classe: str
    codigoOrgaoJulgador: int
    juizoDigital: bool


class PjeSeach(SearchBot):
    """Implemente buscas de processos no sistema PJe.

    Esta classe herda de SearchBot e executa consultas
    utilizando um cliente HTTP para obter dados de processos.
    """

    bot: PJeBot

    @property
    def regiao(self) -> str:
        return self.bot.regiao

    @property
    def is_grau_list(self) -> bool:
        return self.bot._is_grau_list  # noqa: SLF001

    def __call__(
        self,
        data: BotData,
        row: int,
        client: Client,
    ) -> DictResults | None:
        """Realize a busca de um processo no sistema PJe.

        Args:
            data (BotData): Dados do processo a serem consultados.
            row (int): Índice da linha do processo na planilha de entrada.
            client (Client): Instância do cliente HTTP
                para requisições ao sistema PJe.
            regiao (str):regiao

        Returns:
            (DictResults | Literal["Nenhum processo encontrado"]): Resultado da
                busca do processo ou mensagem indicando
                que nenhum processo foi encontrado.

        """
        numero_processo = data["NUMERO_PROCESSO"]
        message = f"Buscando processo {numero_processo}"
        self.print_message(
            message=message,
            row=row,
            message_type="log",
        )

        link = el.LINK_DADOS_BASICOS.format(
            trt_id=self.regiao,
            numero_processo=numero_processo,
        )

        response = client.get(url=link)
        id_processo = self._format_response_pje(response).get("id", "")

        if not id_processo:
            self._print_processo_nao_encontrado(row=row)
            return None

        url_ = el.LINK_CONSULTA_PROCESSO.format(
            trt_id=self.regiao,
            id_processo=id_processo,
        )
        result = client.get(url=url_)

        if result.status_code != HTTP_OK_STATUS:
            self._print_processo_nao_encontrado(row=row)
            return None

        return DictResults(
            id_processo=id_processo,
            data_request=result.json(),
        )

    def _format_response_pje(self, response: Response) -> _ResponseDadosBasicos:

        with suppress(JSONDecodeError):
            if response.status_code != HTTP_OK_STATUS:
                return {}

            data_request = response.json()
            if isinstance(data_request, list):
                data_request: _ResponseDadosBasicos = data_request[0]

            return data_request

        return {}

    def _print_processo_nao_encontrado(self, row: int) -> None:

        msg_type = "error" if not self.is_grau_list else "info"
        self.print_message(
            message="Nenhum processo encontrado",
            message_type=msg_type,
            row=row,
        )
