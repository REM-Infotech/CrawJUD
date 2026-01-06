"""Sistema de envio de logs para o ClientUI."""

from __future__ import annotations

import json
import sys
import traceback
from base64 import b64decode
from contextlib import suppress
from datetime import datetime
from queue import Queue
from threading import Thread
from time import sleep
from typing import TYPE_CHECKING, Literal, TypedDict
from zoneinfo import ZoneInfo

from clear import clear
from dotenv import load_dotenv
from requests import Session
from socketio import Client
from socketio.exceptions import BadNamespaceError
from tqdm import tqdm

from backend.config import settings
from backend.dicionarios import Message
from backend.resources.iterators.queues import QueueIterator

if TYPE_CHECKING:
    from pathlib import Path

    from backend.controllers.head import CrawJUD
    from typings import Any, MessageType
load_dotenv()


MSG_ROBO_INICIADO = "Robô inicializado!"
MSG_FIM_EXECUCAO = "Fim da execução"
MSG_ARQUIVO_BAIXADO = "Arquivo baixado com sucesso!"
MSG_EXECUCAO_SUCESSO = "Execução efetuada com sucesso!"


type MessageStr = Literal[
    "Robô inicializado!",
    "Fim da execução",
    "Arquivo baixado com sucesso!",
    "Execução efetuada com sucesso!",
    "Processo Encontrado!",
]


class Count(TypedDict):
    """Dicionario de contagem."""

    sucessos: int = 0
    remainign_count: int = 0
    erros: int = 0


class PrintMessage:
    """Envio de logs para o FrontEnd."""

    bot: CrawJUD
    _message_type: MessageType

    @property
    def file_log(self) -> Path:
        """Retorne o caminho do arquivo de log do robô.

        Returns:
            Path: Caminho do arquivo de log.

        """
        out_dir = self.bot.output_dir_path
        return out_dir.joinpath(f"{self.bot.pid.upper()}.txt")

    def __init__(self, bot: CrawJUD) -> None:
        """Instancia da queue de salvamento de sucessos."""
        self.bot = bot
        self.queue_print_bot = Queue[Message]()
        self.thread_print_bot = Thread(target=self.print_msg)
        self.thread_print_bot.start()
        self.succcess_count = 0
        self.erros = 0

    def __call__(
        self,
        message: MessageStr | str,
        message_type: MessageType,
        row: int = 0,
        link: str | None = None,
    ) -> None:
        """Envie mensagem formatada para a fila de logs.

        Args:
            message (str): Mensagem a ser enviada.
            message_type (MessageType): Tipo da mensagem.
            row (int): Linha do registro.
            link (str): Link do resultado (apenas no fim da execução)

        """
        _mini_pid = self.bot.pid

        if not row or row == 0:
            row = self.bot.row

        self.message = message
        tz = ZoneInfo("America/Sao_Paulo")
        # Obtém o horário atual formatado
        time_ = datetime.now(tz=tz).strftime("%H:%M:%S:%z")

        msg = Message(
            pid=self.bot.pid,
            row=row,
            message=str(message),
            time_message=time_,
            message_type=message_type,
            status="Em Execução",
            total=self.bot.total_rows,
            sucessos=self.calc_success(message_type),
            erros=self.calc_error(message_type),
            restantes=self.calc_remaining(message_type),
        )
        self.queue_print_bot.put_nowait(msg)

    def calc_success(self, message_type: MessageType) -> int:
        """Calcula o total de mensagens de sucesso.

        Args:
            message_type (MessageType): Tipo da mensagem.

        Returns:
            int: Quantidade de mensagens de sucesso.

        """
        message_sucesso = self.message == MSG_EXECUCAO_SUCESSO
        if message_sucesso and message_type == "success":
            self.succcess_count += 1

        return self.succcess_count

    def calc_error(self, message_type: MessageType) -> int:
        """Calcula o total de mensagens de erro.

        Args:
            message_type (MessageType): Tipo da mensagem.

        Returns:
            int: Quantidade de mensagens de erro.

        """
        message_sucesso = self.message == MSG_EXECUCAO_SUCESSO

        if message_sucesso and message_type == "error":
            self.erros += 1

        return self.erros

    def calc_remaining(self, message_type: MessageType) -> int:
        """Calcula o total de registros restantes.

        Args:
            message_type (MessageType): Tipo da mensagem.

        Returns:
            int: Quantidade de registros restantes.

        """
        message_sucesso = self.message == MSG_EXECUCAO_SUCESSO
        check_msg_type = any([
            message_type == "success",
            message_type == "error",
        ])

        if message_sucesso and check_msg_type and self.bot.remaining > 0:
            self.bot.remaining -= 1

        elif self.message == MSG_FIM_EXECUCAO:
            self.bot.remaining = 0

        return self.bot.remaining

    def _call_set_event(self) -> None:

        self.set_event()

    def print_msg(self) -> None:
        """Envie mensagens de log para o servidor via socket.

        Esta função conecta ao servidor socketio e envia mensagens
        presentes na fila para o FrontEnd.

        """
        socketio_server = settings.get("API_URL")

        cookies = json.loads(
            b64decode(self.bot.config.get("cookies")).decode(),
        )
        session = Session()
        session.headers.update({
            "Authorization": f"Bearer {cookies['access_token_cookie']}",
        })

        sio = Client(http_session=session)
        sio.on(
            "bot_stop",
            self._call_set_event,
            namespace="/bot",
        )

        self.sio = sio
        for data in QueueIterator(self.queue_print_bot):
            sleep(1)
            with suppress(Exception):
                if not sio.connected:
                    sio.connect(
                        url=socketio_server,
                        namespaces=["/bot"],
                        transports=["polling"],
                        wait=True,
                        wait_timeout=5,
                        retry=True,
                    )
                    sio.emit(
                        "join_room",
                        data={"room": self.bot.pid},
                        namespace="/bot",
                    )

            if data:
                with suppress(Exception):
                    to_write = data["message"]
                    mode = "a" if self.file_log.exists() else "w"
                    try:
                        self.emit_message(data, sio)

                    except BadNamespaceError:
                        sio.connect(
                            url=socketio_server,
                            namespaces=["/bot"],
                        )
                        self.emit_message(data, sio)

                    except Exception as e:  # noqa: BLE001
                        clear()
                        to_write = "\n".join(
                            traceback.format_exception(e),
                        )
                        tqdm.write(to_write, file=sys.stdout)

                    with self.file_log.open(
                        mode=mode,
                        encoding="utf-8",
                    ) as fp:
                        tqdm.write(to_write, file=fp)

    def emit_message(self, data: Message, sio: Client) -> None:
        sio.emit("logbot", data=data, namespace="/bot")
        tqdm.write(str(data["message"]), file=sys.stdout)

    def set_event(self, *args: Any, **kwargs: Any) -> None:
        """Evento de parada do robô.

        Args:
            *args (Any): Argumentos posicionais.
            **kwargs (Any): Argumentos nomeados.

        """
        tz = ZoneInfo("America/Sao_Paulo")
        time_ = datetime.now(tz=tz).strftime("%H:%M:%S:%z")

        message = "Encerrando execução..."
        message_type = "warning"

        self.emit_message(
            Message(
                pid=self.bot.pid,
                row=0,
                message=str(message),
                time_message=time_,
                message_type="info",
                status="Em Execução",
                total=self.bot.total_rows,
                sucessos=self.calc_success(message_type),
                erros=self.calc_error(message_type),
                restantes=self.calc_remaining(message_type),
                link="",
            ),
            self.sio,
        )

        self.bot.bot_stopped.set()
