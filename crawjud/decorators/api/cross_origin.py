"""Módulo do decorator CrossDomain."""

from __future__ import annotations

from datetime import timedelta
from functools import update_wrapper
from typing import TYPE_CHECKING

from quart import (
    Response,
    abort,
    current_app,
    make_response,
    request,
)

if TYPE_CHECKING:
    from collections.abc import Callable

    from crawjud.interfaces.types import Methods, P, T


class CrossDomain:
    """Adicione cabeçalhos CORS às respostas HTTP para permitir requisições cross-origin.

    Esta classe fornece métodos utilitários para normalizar métodos, cabeçalhos, origens
    e tempo de cache, além de um decorador para aplicar as regras CORS em rotas HTTP.
    """

    def __init__(
        self,
        origin: str | None = None,
        methods: Methods | None = None,
        headers: list[str] | None = None,
        max_age: int = 21600,
        *,
        attach_to_all: bool = True,
        automatic_options: bool = True,
    ) -> None:
        """Inicializa o objeto CrossDomain com configurações de CORS personalizadas.

        Args:
            origin (str | None): Origem permitida para requisições CORS.
            methods (Methods | None): Métodos HTTP permitidos.
            headers (list[str] | None): Lista de cabeçalhos permitidos.
            max_age (int): Tempo máximo de cache dos cabeçalhos CORS em segundos.
            attach_to_all (bool): Se deve anexar cabeçalhos a todas as respostas.
            automatic_options (bool): Se deve gerar resposta automática para OPTIONS.

        """
        self.origin = origin
        self.methods = methods
        self.headers = headers
        self.max_age = 21600
        self.attach_to_all = attach_to_all
        self.automatic_options = automatic_options

    def __call__(
        self,
        wrapped_function: Callable[P, T],
    ) -> Callable[P, Callable[P, T | None]]:
        """Adiciona cabeçalhos CORS à resposta HTTP.

        Args:
            wrapped_function (Callable[P, T]): Função a ser decorada para receber os
                cabeçalhos CORS.
            origin (str | None): Origem permitida para CORS.
            methods (list[str] | None): Métodos HTTP permitidos.
            headers (list[str] | None): Cabeçalhos permitidos.
            max_age (int): Tempo máximo de cache dos cabeçalhos CORS.
            attach_to_all (bool): Se deve anexar cabeçalhos a todas respostas.
            automatic_options (bool): Se deve gerar resposta automática para OPTIONS.

        Returns:
            Callable: Decorador que adiciona cabeçalhos CORS à resposta.

        """
        normalized_methods = self._normalize_methods(self.methods)
        normalized_headers = self._normalize_headers(self.headers)
        normalized_origin = self._normalize_origin(self.origin)
        normalized_max_age = self._normalize_max_age(self.max_age)

        async def _wrapped(
            *args: P.args,
            **kwargs: P.kwargs,
        ) -> Response:
            if self.automatic_options and request.method == "OPTIONS":
                resp = await self._handle_options()
            elif request.method == "POST":
                resp = await self._handle_post(
                    wrapped_function,
                    *args,
                    **kwargs,
                )
            else:
                resp = await make_response(
                    await wrapped_function(*args, **kwargs),
                )

            if not self.attach_to_all and request.method != "OPTIONS":
                return await resp

            self._set_cors_headers(
                resp,
                normalized_origin,
                normalized_methods,
                normalized_headers,
                normalized_max_age,
            )
            return resp

        wrapped_function.provide_automatic_options = False
        return update_wrapper(_wrapped, wrapped_function)

    def _normalize_methods(self, methods: list[str] | None) -> str | None:
        """Normaliza os métodos HTTP para cabeçalho CORS.

        Args:
            methods (list[str] | None): Lista de métodos HTTP ou None.

        Returns:
            str | None: Métodos HTTP normalizados em string ou None.

        """
        return (
            ", ".join(sorted(x.upper() for x in methods)) if methods else None
        )

    def _normalize_headers(self, headers: list[str] | None) -> str | None:
        """Normaliza os cabeçalhos para CORS.

        Args:
            headers (list[str] | None): Lista de cabeçalhos HTTP ou None.

        Returns:
            str | None: Cabeçalhos normalizados em string ou None.

        """
        if headers and not isinstance(headers, str):
            return ", ".join(x.upper() for x in headers)
        return headers

    def _normalize_origin(self, origin: str | None) -> str | None:
        """Normaliza a origem para CORS.

        Args:
            origin (str | None): Origem permitida para CORS.

        Returns:
            str | None: Origem normalizada como string ou None.

        """
        if isinstance(origin, str):
            return origin
        if origin:
            return ", ".join(origin)
        return None

    def _normalize_max_age(self, max_age: int | timedelta) -> int:
        """Normaliza o tempo máximo de cache para CORS.

        Args:
            max_age (int | timedelta): Tempo máximo de cache em segundos ou timedelta.

        Returns:
            int: Tempo máximo de cache em segundos.

        """
        return (
            int(max_age.total_seconds())
            if isinstance(max_age, timedelta)
            else max_age
        )

    def _get_methods(self, normalized_methods: str | None) -> str:
        """Obtém os métodos permitidos para CORS.

        Returns:
            str: Métodos HTTP permitidos, formatados para cabeçalho CORS.

        """
        if normalized_methods is not None:
            return normalized_methods
        options_resp = current_app.make_default_options_response()
        return options_resp.headers["allow"]

    async def _handle_options() -> Response:
        """Gera resposta para método OPTIONS.

        Returns:
            Response: Resposta padrão para o método OPTIONS.

        """
        return await current_app.make_default_options_response()

    async def _handle_post(
        self,
        f: Callable,
        *args: T,
        **kwargs: T,
    ) -> Response:
        """Processa requisição POST com verificação de XSRF.

        Returns:
            Response: Resposta HTTP gerada após o processamento do POST.

        """
        name_ = f.__globals__.get("__name__")
        if name_ == "quart_jwt_extended.view_decorators":
            cookie_xsrf_name = current_app.config.get(
                "JWT_ACCESS_CSRF_COOKIE_NAME",
            )
            header_xsrf_name = current_app.config.get(
                "JWT_ACCESS_CSRF_HEADER_NAME",
            )
            xsrf_token = request.cookies.get(cookie_xsrf_name, None)
            if not xsrf_token:
                abort(401, message="Missing XSRF Token")
            request.headers.set(header_xsrf_name, xsrf_token)
        return await make_response(await f(*args, **kwargs))

    def _set_cors_headers(
        self,
        resp: Response,
        normalized_origin: str | None,
        normalized_methods: str | None,
        normalized_headers: str | None,
        normalized_max_age: int,
    ) -> None:
        """Define os cabeçalhos CORS na resposta."""
        h = resp.headers

        methods = self._get_methods(normalized_methods)
        h["Access-Control-Allow-Origin"] = normalized_origin
        h["Access-Control-Allow-Methods"] = methods
        h["Access-Control-Max-Age"] = str(normalized_max_age)
        if normalized_headers is not None:
            h["Access-Control-Allow-Headers"] = normalized_headers
