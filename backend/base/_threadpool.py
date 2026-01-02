from __future__ import annotations

from concurrent.futures import Future, ThreadPoolExecutor
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable


class CrawJudPoolExecutor[**P, R](ThreadPoolExecutor):
    def submit(
        self,
        fn: Callable[P, R],
        /,
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> Future[R]:

        self._args = args
        self._kwargs = kwargs

        return super().submit(fn, *args, **kwargs)
