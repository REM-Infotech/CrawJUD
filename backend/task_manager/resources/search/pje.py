"""Implemente buscas de processos no sistema PJe.

Este módulo contém classes e funções para consultar processos
no sistema PJe utilizando um cliente HTTP.
"""

from __future__ import annotations

from contextlib import suppress
from json.decoder import JSONDecodeError
from typing import TYPE_CHECKING, TypedDict

from backend.task_manager.constants import HTTP_OK_STATUS
from backend.task_manager.interfaces.pje import DictResults
from backend.task_manager.resources.elements import pje as el
from backend.task_manager.resources.search.main import SearchBot

if TYPE_CHECKING:
    from httpx import Client, Response

    from backend.task_manager.controllers import PJeBot


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

    def __call__(
        self,
        data: dict,
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
            self.print_message(
                message="Nenhum processo encontrado",
                message_type="error",
                row=row,
            )
            return None

        url_ = el.LINK_CONSULTA_PROCESSO.format(
            trt_id=self.regiao,
            id_processo=id_processo,
        )
        result = client.get(url=url_)

        if result.status_code != HTTP_OK_STATUS:
            self.print_message(
                message="Nenhum processo encontrado",
                message_type="error",
                row=row,
            )
            return None

        return DictResults(
            id_processo=id_processo,
            data_request=result.json(),
        )

    def _format_response_pje(self, response: Response) -> _ResponseDadosBasicos:

        with suppress(JSONDecodeError):
            data_request = response.json()
            if isinstance(data_request, list):
                data_request: _ResponseDadosBasicos = data_request[0]

            return data_request

        return {}
