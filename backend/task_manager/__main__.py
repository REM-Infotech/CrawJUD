"""Main entry point for the Task Manager application."""

import threading
from time import perf_counter

from celery.apps.worker import Worker

from backend.task_manager import make_celery

THIRTY_SECONDS = 600


app = make_celery()

worker = Worker(app=app)
threading.Thread(target=worker.start).start()
start_time = 0

while True:
    if start_time == 0:
        start_time = perf_counter()

    end_time = perf_counter()

    # Verifica se ja passaram 30 segundos
    if end_time - start_time >= THIRTY_SECONDS:
        start_time = perf_counter()  # Reseta o tempo inicial
