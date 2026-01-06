# ruff: noqa: N802

"""Módulo de controle de protocolos."""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from celery import Celery

type Any = any


class CeleryTask[**P, R](Protocol[P, R]):
    """Defina o protocolo para tasks Celery genéricas."""

    def __call__[**P, T](self, *args: P.args, **kwargs: P.kwargs) -> R: ...

    @classmethod
    def bind(cls, app: Celery) -> None:
        """Vincule a task ao app Celery."""
        ...

    @classmethod
    def on_bound(cls, app: Celery) -> None:
        """Execute ações adicionais ao vincular a task ao app."""
        ...

    @classmethod
    def _get_app(cls) -> None:
        """Obtenha a instância do app Celery."""
        ...

    @classmethod
    def annotate(cls) -> None:
        """Anote a task com metadados adicionais."""
        ...

    @classmethod
    def add_around(cls, attr: str, around: Any) -> None:
        """Adicione lógica ao redor de um atributo da task."""
        ...

    def run(self, *args: Any, **kwargs: Any) -> None:
        """Execute o corpo da task Celery."""
        ...

    def start_strategy(
        self,
        app: Any,
        consumer: Any,
        **kwargs: Any,
    ) -> None:
        """Inicie a estratégia de execução da task."""
        ...

    def delay(self, *args: Any, **kwargs: Any) -> Any:
        """Execute a task de forma assíncrona (atalho para apply_async).

        Retorna:
            AsyncResult: Resultado futuro da execução.
        """
        ...

    def apply_async(
        self,
        *,
        args: tuple[Any, ...] | None = None,
        kwargs: dict[str, Any] | None = None,
        task_id: str | None = None,
        producer: Any | None = None,
        link: Any | None = None,
        link_error: Any | None = None,
        shadow: str | None = None,
        **options: Any,
    ) -> Any:
        """Agende a execução assíncrona da task.

        Args:
            args (Tuple): Argumentos posicionais.
            kwargs (Dict): Argumentos nomeados.
            task_id (str, opcional): Id da task.
            producer (Any, opcional): Produtor customizado.
            link (Any, opcional): Task(s) a executar em sucesso.
            link_error (Any, opcional): Task(s) a executar em erro.
            shadow (str, opcional): Nome alternativo para logs.
            **options: Opções adicionais.

        Retorna:
            AsyncResult: Resultado futuro da execução.

        Raises:
            TypeError: Argumentos inválidos.
            ValueError: Limite de tempo inválido.
            OperationalError: Falha de conexão.

        """
        ...

    def shadow_name(
        self,
        args: tuple[Any, ...],
        kwargs: dict[str, Any],
        options: dict[str, Any],
    ) -> Any:
        """Retorne nome customizado da task para logs/monitoramento."""
        ...

    def retry(
        self,
        *,
        args: tuple[Any, ...] | None = None,
        kwargs: dict[str, Any] | None = None,
        exc: Exception | None = None,
        throw: bool = True,
        eta: Any | None = None,
        countdown: float | None = None,
        max_retries: int | None = None,
        **options: Any,
    ) -> None:
        """Reagende a execução da task para nova tentativa.

        Args:
            args (Tuple, opcional): Argumentos posicionais.
            kwargs (Dict, opcional): Argumentos nomeados.
            exc (Exception, opcional): Exceção customizada.
            throw (bool, opcional): Lança exceção Retry.
            eta (Any, opcional): Data/hora para retry.
            countdown (float, opcional): Segundos para retry.
            max_retries (int, opcional): Máximo de tentativas.
            **options: Opções extras.

        Raises:
            Retry: Sempre lançada para indicar retry.

        """
        ...

    def apply(
        self,
        *,
        args: tuple[Any, ...] | None = None,
        kwargs: dict[str, Any] | None = None,
        link: Any | None = None,
        link_error: Any | None = None,
        task_id: str | None = None,
        retries: int | None = None,
        throw: bool | None = None,
        logfile: Any | None = None,
        loglevel: Any | None = None,
        headers: dict[str, Any] | None = None,
        **options: Any,
    ) -> Any:
        """Execute a task localmente e bloqueie até o retorno.

        Args:
            args (Tuple, opcional): Argumentos posicionais.
            kwargs (Dict, opcional): Argumentos nomeados.
            link (Any, opcional): Task(s) a executar em sucesso.
            link_error (Any, opcional): Task(s) a executar em erro.
            task_id (str, opcional): Id da task.
            retries (int, opcional): Tentativas.
            throw (bool, opcional): Propaga exceção.
            logfile (Any, opcional): Log customizado.
            loglevel (Any, opcional): Nível do log.
            headers (Dict, opcional): Cabeçalhos customizados.
            **options: Opções extras.

        Retorna:
            EagerResult: Resultado imediato da execução.

        """
        ...

    def AsyncResult(self, task_id: str, **kwargs: Any) -> None:
        """Obtenha AsyncResult para o id da tarefa especificada.

        Args:
            task_id (str): Id da tarefa para obter o resultado.
            **kwargs: Argumentos adicionais para configuração.

        """
        ...

    def signature(
        self,
        args: tuple[Any, ...] | None = None,
        *starargs: Any,
        **starkwargs: Any,
    ) -> None:
        """Crie uma assinatura para a task."""
        ...

    subtask = signature

    def s(self, *args: Any, **kwargs: Any) -> None:
        """Crie uma assinatura para a task (atalho)."""
        ...

    def si(self, *args: Any, **kwargs: Any) -> None:
        """Crie assinatura imutável para a task."""
        ...

    def chunks(self, it: Any, n: int) -> Any:
        """Crie task de chunks para processamento em lotes."""
        ...

    def map(self, it: Any) -> Any:
        """Crie task de map para processamento iterativo."""
        ...

    def starmap(self, it: Any) -> Any:
        """Crie task de starmap para processamento iterativo."""
        ...

    def send_event(
        self,
        *,
        type_: str,
        retry: bool = True,
        retry_policy: Any | None = None,
        **fields: Any,
    ) -> None:
        """Envie evento de monitoramento customizado.

        Args:
            type_ (str): Tipo do evento.
            retry (bool, opcional): Tentar novamente em falha.
            retry_policy (Any, opcional): Política de retry.
            **fields: Campos adicionais do evento.

        """
        ...

    def replace(self, sig: Any) -> None:
        """Substitua esta task por outra mantendo o mesmo id.

        Args:
            sig (Any): Assinatura substituta.

        """
        ...

    def add_to_chord(self, sig: Any, *, lazy: bool = False) -> None:
        """Adicione assinatura ao chord da task.

        Args:
            sig (Any): Assinatura a adicionar.
            lazy (bool, opcional): Não executar imediatamente.

        """
        ...

    def update_state(
        self,
        task_id: str | None = None,
        state: str | None = None,
        meta: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> None:
        """Atualize o estado da task.

        Args:
            task_id (str, opcional): Id da task.
            state (str, opcional): Novo estado.
            meta (Dict, opcional): Metadados do estado.
            **kwargs: Argumentos adicionais.

        """
        ...

    def before_start(
        self,
        task_id: str,
        args: tuple[Any, ...],
        kwargs: dict[str, Any],
    ) -> None:
        """Execute ação antes de iniciar a task.

        Args:
            task_id (str): Id da task.
            args (Tuple): Argumentos originais.
            kwargs (Dict): Argumentos nomeados originais.

        """
        ...

    def on_success(
        self,
        retval: Any,
        task_id: str,
        args: tuple[Any, ...],
        kwargs: dict[str, Any],
    ) -> None:
        """Execute ação ao finalizar a task com sucesso.

        Args:
            retval (Any): Valor de retorno.
            task_id (str): Id da task.
            args (Tuple): Argumentos originais.
            kwargs (Dict): Argumentos nomeados originais.

        """
        ...

    def on_retry(
        self,
        exc: Exception,
        task_id: str,
        args: tuple[Any, ...],
        kwargs: dict[str, Any],
        einfo: Any,
    ) -> None:
        """Execute ação ao tentar novamente a task.

        Args:
            exc (Exception): Exceção de retry.
            task_id (str): Id da task.
            args (Tuple): Argumentos originais.
            kwargs (Dict): Argumentos nomeados originais.
            einfo (Any): Informações da exceção.

        """
        ...

    def on_failure(
        self,
        exc: Exception,
        task_id: str,
        args: tuple[Any, ...],
        kwargs: dict[str, Any],
        einfo: Any,
    ) -> None:
        """Execute ação ao falhar a task.

        Args:
            exc (Exception): Exceção lançada.
            task_id (str): Id da task.
            args (Tuple): Argumentos originais.
            kwargs (Dict): Argumentos nomeados originais.
            einfo (Any): Informações da exceção.

        """
        ...

    def after_return(
        self,
        status: str,
        retval: Any,
        task_id: str,
        args: tuple[Any, ...],
        kwargs: dict[str, Any],
        einfo: Any,
    ) -> None:
        """Execute ação após o retorno da task.

        Args:
            status (str): Estado atual.
            retval (Any): Valor/erro retornado.
            task_id (str): Id da task.
            args (Tuple): Argumentos originais.
            kwargs (Dict): Argumentos nomeados originais.
            einfo (Any): Informações da exceção.

        """
        ...

    def on_replace(self, sig: Any) -> None:
        """Execute ação ao substituir a task."""
        ...

    def add_trail(self, result: Any) -> None:
        """Adicione resultado ao trail da task."""
        ...

    def push_request(self, *args: Any, **kwargs: Any) -> None:
        """Empilhe uma nova requisição para a task."""
        ...

    def pop_request(self) -> Any:
        """Remova a requisição do topo da pilha."""
        ...

    def _get_request(self) -> Any:
        """Obtenha a requisição atual da task."""
        ...

    def _get_exec_options(self) -> Any:
        """Obtenha opções de execução da task."""
        ...

    @property
    def backend(self) -> Any:
        """Obtenha o backend da task."""
        ...

    @backend.setter
    def backend(self, value: Any) -> None:
        """Defina o backend da task."""
        ...
