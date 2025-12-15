"""Inicie a aplicação Flask e o servidor SocketIO.

Este script é o ponto de entrada principal para a API. Ele cria a aplicação,
carrega as rotas e executa o servidor SocketIO na porta definida.
"""

from __future__ import annotations

from threading import Thread

from ._threads import _api, _celery_worker


def _start_backend() -> dict[str, list[Thread]]:

    api_ = Thread(target=_api, daemon=True)
    celery_ = Thread(target=_celery_worker, daemon=True)

    api_.start()
    celery_.start()

    return {"threads": [api_, celery_]}


__all__ = ["_start_backend"]
