from __future__ import annotations

from collections import UserString
from datetime import datetime
from typing import TYPE_CHECKING
from zoneinfo import ZoneInfo

if TYPE_CHECKING:
    from backend.dicionarios import DocumentoPJe

    from ._timeline import TimeLinePJe

TZ_SAO_PAULO = ZoneInfo("America/Sao_Paulo")


class LinkPJe(UserString):
    def __init__(
        self,
        regiao: str,
        id_proc: str,
        query: str,
        endpoint: str,
    ) -> None:
        seq = f"https://pje.trt{regiao}.jus.br/pje-comum-api/api/processos/id/{id_proc}/{endpoint}?{query}"
        super().__init__(seq)

    def __repr__(self) -> str:
        return f"<LinkPJe({self.data})>"


class NomeDocumentoPJe(UserString):
    NOME_DOCUMENTO = "{ANO} - {TIPO} - {PROCESSO} - {TITULO} - {PID} - {ID_UNICO}.pdf"

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
            "id_unico": documento["codigoDocumento"],
            "pid": tl.bot.pid,
        }
        if titulo == tipo:
            seq_dict.pop("titulo")

        seq = f"{' - '.join(seq_dict.values())}.pdf"

        super().__init__(seq)
