"""Sistema de envio de logs para o ClientUI."""

from __future__ import annotations

import traceback
from contextlib import suppress
from queue import Queue
from threading import Thread
from typing import TYPE_CHECKING, TypedDict

from clear import clear
from dotenv import load_dotenv
from socketio import Client
from socketio.exceptions import BadNamespaceError
from tqdm import tqdm

from backend.task_manager.config import config
from backend.task_manager.interfaces import Message
from backend.task_manager.resources.iterators.queues import QueueIterator
from backend.task_manager.types_app import MessageLog, MessageType

if TYPE_CHECKING:
    from pathlib import Path

    from backend.api.types_app import AnyType
    from backend.task_manager.controllers.head import CrawJUD

load_dotenv()

MSG_ROBO_INICIADO = "Robô inicializado!"
MSG_FIM_EXECUCAO = "Fim da execução"
MSG_ARQUIVO_BAIXADO = "Arquivo baixado com sucesso!"
MSG_EXECUCAO_SUCESSO = "Execução Efetuada com sucesso!"


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
        self.queue_print_bot = Queue()
        self.thread_print_bot = Thread(target=self.print_msg)
        self.thread_print_bot.start()
        self.succcess_count = 0
        self.erros = 0

    def __call__(
        self,
        message: str,
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
        mini_pid = self.bot.pid

        if not row or row == 0:
            row = self.bot.row

        self.message = message
        message = MessageLog(message).format(
            mini_pid,
            message_type,
            row,
        )

        msg = Message(
            pid=self.bot.pid,
            row=row,
            message=str(message),
            message_type=message_type,
            status="Em Execução",
            total=self.bot.total_rows,
            sucessos=self.calc_success(message_type),
            erros=self.calc_error(message_type),
            restantes=self.calc_remaining(message_type),
            link=link,
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

    def print_msg(self) -> None:
        """Envie mensagens de log para o servidor via socket.

        Esta função conecta ao servidor socketio e envia mensagens
        presentes na fila para o FrontEnd.

        """
        socketio_server = config.get("API_URL")
        sio = Client()
        sio.on(
            "bot_stop",
            self.set_event,
            namespace="/bot_logs",
        )
        sio.connect(url=socketio_server, namespaces=["/bot_logs"])
        sio.emit(
            "join_room",
            data={"room": self.bot.pid},
            namespace="/bot_logs",
        )

        for data in QueueIterator[Message](self.queue_print_bot):
            if data:
                with suppress(Exception):
                    to_write = data["message"]
                    mode = "a" if self.file_log.exists() else "w"
                    try:
                        self.emit_message(data, sio)

                    except BadNamespaceError:
                        sio.connect(
                            url=socketio_server,
                            namespaces=["/bot_logs"],
                        )
                        self.emit_message(data, sio)

                    except Exception as e:
                        clear()

                        exc = "\n".join(traceback.format_exception(e))
                        print(exc)  # noqa: T201
                        to_write = exc

                    with self.file_log.open(mode=mode, encoding="utf-8") as fp:
                        tqdm.write(to_write, file=fp)

    def emit_message(self, data: Message, sio: Client) -> None:

        sio.emit("logbot", data=data, namespace="/bot_logs")
        print(data["message"])  # noqa: T201

    def set_event(self, *args: AnyType, **kwargs: AnyType) -> None:
        """Evento de parada do robô.

        Args:
            *args (AnyType): Argumentos posicionais.
            **kwargs (AnyType): Argumentos nomeados.

        """
        self.bot.bot_stopped.set()
