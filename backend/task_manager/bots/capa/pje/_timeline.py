from __future__ import annotations

from collections import UserString
from contextlib import suppress
from datetime import datetime
from typing import TYPE_CHECKING, Any, Literal, Self, cast
from zoneinfo import ZoneInfo

if TYPE_CHECKING:
    from httpx import Client

    from backend.task_manager.bots.capa.pje._dicionarios import DocumentoPJe
    from backend.task_manager.controllers import PJeBot

type AnyType = Any


TZ_SAO_PAULO = ZoneInfo("America/Sao_Paulo")

type ReprLinkTimeline = Literal[
    "LinkPJe<https://pje.trt{regiao}.jus.br/pje-comum-api/api/processos/id/{id_proc}/{endpoint}?{query}>"
]


class LinkPJe(UserString):
    def __init__(
        self,
        regiao: str,
        id_proc: str,
        query: dict,
        endpoint: str,
    ) -> None:
        seq = f"https://pje.trt{regiao}.jus.br/pje-comum-api/api/processos/id/{id_proc}/{endpoint}?{query}"
        super().__init__(seq)

    def __repr__(self) -> ReprLinkTimeline:
        return f"<LinkPJe({self.data})>"


class NomeDocumentoPJe(UserString):
    NOME_DOCUMENTO = "{ANO} - {TIPO} - {PROCESSO} - {TITULO} - {PID}.pdf"

    def __init__(self, tl: TimeLinePJe, documento: DocumentoPJe) -> None:
        ano = datetime.now(tz=TZ_SAO_PAULO).strftime("%Y")
        tipo = documento["tipo"]
        titulo = documento["titulo"]
        splited_titulo = titulo.split(" - ")[1:] if " - " in titulo else [titulo]
        titulo_formatado = " ".join([i.capitalize() for i in splited_titulo])

        seq_dict = {
            "ano": ano,
            "tipo": tipo,
            "processo": tl.processo,
            "titulo": titulo_formatado,
            "pid": tl.bot.pid,
            "id_doc": documento["idUnicoDocumento"],
        }
        if titulo == tipo:
            seq_dict.pop("titulo")

        seq = f"{' - '.join(seq_dict.values())}.pdf"

        super().__init__(seq)


class TimeLinePJe:
    documentos: list[DocumentoPJe]

    def __init__(
        self,
        id_processo: str,
        regiao: str,
        processo: str,
        cliente: Client,
        bot: PJeBot,
    ) -> None:
        self.id_processo = id_processo
        self.regiao = regiao
        self.processo = processo
        self.cliente = cliente
        self.bot = bot

    @classmethod
    def load(
        cls,
        bot: PJeBot,
        cliente: Client,
        id_processo: int | str,
        regiao: str,
        processo: str,
        *,
        apenas_assinados: bool = True,
        buscar_movimentos: bool = True,
        buscar_documentos: bool = True,
    ) -> Self:
        self = cls(
            id_processo=id_processo,
            regiao=regiao,
            processo=processo,
            cliente=cliente,
            bot=bot,
        )

        query_arguments = "&".join([
            "=".join(["buscarMovimentos", str(buscar_movimentos).lower()]),
            "=".join(["buscarDocumentos", str(buscar_documentos).lower()]),
            "=".join([
                "somenteDocumentosAssinados",
                str(apenas_assinados).lower(),
            ]),
        ])

        link = str(LinkPJe(regiao, id_processo, query_arguments, "timeline"))

        self.result = cliente.get(link)
        with suppress(Exception):
            self.result = cast("list[DocumentoPJe]", self.result.json())
            self.documentos = list(
                filter(lambda x: x.get("idUnicoDocumento"), self.result),
            )

        return self

    def baixar_documento(
        self,
        bot: PJeBot,
        documento: DocumentoPJe,
        grau: str = 1,
        *,
        incluir_capa: bool = False,
        inclur_assinatura: bool = False,
    ) -> bytes:
        query = "&".join([
            f"grau={grau}",
            "=".join(["incluirCapa", str(incluir_capa).lower()]),
            "=".join(["incluir_assinatura", str(inclur_assinatura).lower()]),
        ])

        # Região processo
        r = self.regiao

        # Id interno do processo
        p = self.id_processo

        # Id interno documento
        d = documento["id"]
        link = str(LinkPJe(r, p, query, f"documentos/id/{d}/conteudo"))

        out_dir = bot.output_dir_path
        nome_arquivo = str(NomeDocumentoPJe(tl=self, documento=documento))
        caminho_arquivo = out_dir.joinpath(self.processo, nome_arquivo)

        caminho_arquivo.parent.mkdir(exist_ok=True, parents=True)

        bot.download_file(
            file=str(caminho_arquivo),
            link=link,
            cookies=self.cliente.cookies,
        )
