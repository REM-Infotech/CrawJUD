from __future__ import annotations

from contextlib import suppress
from typing import TYPE_CHECKING, Any, ClassVar, Self, cast

from backend.dicionarios import DocumentoPJe, MovimentacaoPJe

from ._strings import LinkPJe, NomeDocumentoPJe

if TYPE_CHECKING:
    from httpx import Client

    from backend.controllers import PJeBot


type AnyType = Any


BUFFER_1MB = 1024 * 1024
CHUNK_8MB = 8192 * 1024


class TimeLinePJe:
    documentos: ClassVar[list[DocumentoPJe]] = []
    result: ClassVar[list[DocumentoPJe | MovimentacaoPJe]] = []
    movimentacoes: ClassVar[list[MovimentacaoPJe]] = []

    def __init__(
        self,
        id_processo: str,
        regiao: str,
        processo: str,
        cliente: Client,
        bot: PJeBot,
        grau: int,
    ) -> None:
        self.id_processo = id_processo
        self.regiao = regiao
        self.processo = processo
        self.cliente = cliente
        self.bot = bot
        self.grau = grau

    @classmethod
    def load(
        cls,
        *,
        bot: PJeBot,
        cliente: Client,
        id_processo: int | str,
        regiao: str,
        processo: str,
        apenas_assinados: bool = True,
        buscar_movimentos: bool = True,
        buscar_documentos: bool = True,
        grau: int,
    ) -> Self:
        self = cls(
            id_processo=id_processo,
            regiao=regiao,
            processo=processo,
            cliente=cliente,
            bot=bot,
            grau=grau,
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
        with suppress(Exception):
            self.result = cast(
                "list[DocumentoPJe | MovimentacaoPJe]",
                cliente.get(link).json(),
            )
            result2 = list(
                filter(lambda x: x.get("idUnicoDocumento"), self.result),
            )
            self.documentos = [DocumentoPJe(**item) for item in result2]
            self.movimentacoes = [
                MovimentacaoPJe(NUMERO_PROCESSO=processo, INSTANCIA=grau, **item)
                for item in list(
                    filter(lambda x: not x.get("idUnicoDocumento"), self.result),
                )
            ]

        return self

    def baixar_documento(
        self,
        documento: DocumentoPJe,
        grau: str = 1,
        row: int = 0,
        *,
        incluir_capa: bool = False,
        inclur_assinatura: bool = False,
    ) -> None:

        nome_arquivo = str(NomeDocumentoPJe(tl=self, documento=documento))
        msg_ = f'Baixando arquivo "{nome_arquivo}"'
        type_ = "log"
        self.bot.print_message(msg_, type_, row)

        bot = self.bot
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

        stream_kw = {
            "method": "GET",
            "url": link,
        }

        out_dir = bot.output_dir_path

        caminho_arquivo = out_dir.joinpath(self.processo, nome_arquivo)

        caminho_arquivo.parent.mkdir(exist_ok=True, parents=True)

        with (
            self.cliente.stream(**stream_kw) as stream,
            caminho_arquivo.open("wb", buffering=BUFFER_1MB) as fp,
        ):
            for chunk in stream.iter_bytes(chunk_size=CHUNK_8MB):
                fp.write(chunk)

        msg_ = f'Arquivo "{nome_arquivo}" baixado com sucesso!'
        type_ = "info"
        self.bot.print_message(msg_, type_, row)
