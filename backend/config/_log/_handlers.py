import logging
from logging import Handler, LogRecord
from typing import ClassVar


class RichQueueHandler(Handler):
    level: int = logging.INFO

    markups: ClassVar[dict[int, str]] = {
        logging.INFO: "\033[37m{msg}\033[0m",  # white
        logging.ERROR: "\033[31m{msg}\033[0m",  # red
        logging.WARNING: "\033[33m{msg}\033[0m",  # yellow
        logging.DEBUG: "\033[32m{msg}\033[0m",  # green
    }

    def __init__(self, target: str, level: int = logging.INFO) -> None:
        super().__init__()
        self.target = target
        self.level = level

    def emit(self, record: LogRecord) -> None:
        msg = self.format(record)
        msg = self.markups[record.levelno].format(msg=msg)
