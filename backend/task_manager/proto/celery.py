"""Módulo de controle de protocolos."""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

from backend.task_manager.types_app import AnyType, P

if TYPE_CHECKING:
    from celery import Celery


class CeleryTask[T](Protocol[P, T]):
    """Defina o protocolo para tasks Celery genéricas."""

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
    def add_around(cls, attr: str, around: AnyType) -> None:
        """Adicione lógica ao redor de um atributo da task."""
        ...

    def run(self, *args: AnyType, **kwargs: AnyType) -> None:
        """Execute o corpo da task Celery."""
        ...

    def start_strategy(
        self,
        app: AnyType,
        consumer: AnyType,
        **kwargs: AnyType,
    ) -> None:
        """Inicie a estratégia de execução da task."""
        ...

    def delay(self, *args: AnyType, **kwargs: AnyType) -> AnyType:
        """Execute a task de forma assíncrona (atalho para apply_async).

        Retorna:
            AsyncResult: Resultado futuro da execução.
        """
        ...

    def apply_async(
        self,
        *,
        args: tuple[AnyType, ...] | None = None,
        kwargs: dict[str, AnyType] | None = None,
        task_id: str | None = None,
        producer: AnyType | None = None,
        link: AnyType | None = None,
        link_error: AnyType | None = None,
        shadow: str | None = None,
        **options: AnyType,
    ) -> AnyType:
        """Agende a execução assíncrona da task.

        Args:
            args (Tuple): Argumentos posicionais.
            kwargs (Dict): Argumentos nomeados.
            task_id (str, opcional): Id da task.
            producer (AnyType, opcional): Produtor customizado.
            link (AnyType, opcional): Task(s) a executar em sucesso.
            link_error (AnyType, opcional): Task(s) a executar em erro.
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
        args: tuple[AnyType, ...],
        kwargs: dict[str, AnyType],
        options: dict[str, AnyType],
    ) -> AnyType:
        """Retorne nome customizado da task para logs/monitoramento."""
        ...

    def retry(
        self,
        *,
        args: tuple[AnyType, ...] | None = None,
        kwargs: dict[str, AnyType] | None = None,
        exc: Exception | None = None,
        throw: bool = True,
        eta: AnyType | None = None,
        countdown: float | None = None,
        max_retries: int | None = None,
        **options: AnyType,
    ) -> None:
        """Reagende a execução da task para nova tentativa.

        Args:
            args (Tuple, opcional): Argumentos posicionais.
            kwargs (Dict, opcional): Argumentos nomeados.
            exc (Exception, opcional): Exceção customizada.
            throw (bool, opcional): Lança exceção Retry.
            eta (AnyType, opcional): Data/hora para retry.
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
        args: tuple[AnyType, ...] | None = None,
        kwargs: dict[str, AnyType] | None = None,
        link: AnyType | None = None,
        link_error: AnyType | None = None,
        task_id: str | None = None,
        retries: int | None = None,
        throw: bool | None = None,
        logfile: AnyType | None = None,
        loglevel: AnyType | None = None,
        headers: dict[str, AnyType] | None = None,
        **options: AnyType,
    ) -> AnyType:
        """Execute a task localmente e bloqueie até o retorno.

        Args:
            args (Tuple, opcional): Argumentos posicionais.
            kwargs (Dict, opcional): Argumentos nomeados.
            link (AnyType, opcional): Task(s) a executar em sucesso.
            link_error (AnyType, opcional): Task(s) a executar em erro.
            task_id (str, opcional): Id da task.
            retries (int, opcional): Tentativas.
            throw (bool, opcional): Propaga exceção.
            logfile (AnyType, opcional): Log customizado.
            loglevel (AnyType, opcional): Nível do log.
            headers (Dict, opcional): Cabeçalhos customizados.
            **options: Opções extras.

        Retorna:
            EagerResult: Resultado imediato da execução.

        """
        ...

    def AsyncResult(self, task_id: str, **kwargs: AnyType) -> None:
        """Obtenha AsyncResult para o id da tarefa especificada.

        Args:
            task_id (str): Id da tarefa para obter o resultado.
            **kwargs: Argumentos adicionais para configuração.

        """
        ...

    def signature(
        self,
        args: tuple[AnyType, ...] | None = None,
        *starargs: AnyType,
        **starkwargs: AnyType,
    ) -> None:
        """Crie uma assinatura para a task."""
        ...

    subtask = signature

    def s(self, *args: AnyType, **kwargs: AnyType) -> None:
        """Crie uma assinatura para a task (atalho)."""
        ...

    def si(self, *args: AnyType, **kwargs: AnyType) -> None:
        """Crie assinatura imutável para a task."""
        ...

    def chunks(self, it: AnyType, n: int) -> AnyType:
        """Crie task de chunks para processamento em lotes."""
        ...

    def map(self, it: AnyType) -> AnyType:
        """Crie task de map para processamento iterativo."""
        ...

    def starmap(self, it: AnyType) -> AnyType:
        """Crie task de starmap para processamento iterativo."""
        ...

    def send_event(
        self,
        *,
        type_: str,
        retry: bool = True,
        retry_policy: AnyType | None = None,
        **fields: AnyType,
    ) -> None:
        """Envie evento de monitoramento customizado.

        Args:
            type_ (str): Tipo do evento.
            retry (bool, opcional): Tentar novamente em falha.
            retry_policy (AnyType, opcional): Política de retry.
            **fields: Campos adicionais do evento.

        """
        ...

    def replace(self, sig: AnyType) -> None:
        """Substitua esta task por outra mantendo o mesmo id.

        Args:
            sig (AnyType): Assinatura substituta.

        """
        ...

    def add_to_chord(self, sig: AnyType, *, lazy: bool = False) -> None:
        """Adicione assinatura ao chord da task.

        Args:
            sig (AnyType): Assinatura a adicionar.
            lazy (bool, opcional): Não executar imediatamente.

        """
        ...

    def update_state(
        self,
        task_id: str | None = None,
        state: str | None = None,
        meta: dict[str, AnyType] | None = None,
        **kwargs: AnyType,
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
        args: tuple[AnyType, ...],
        kwargs: dict[str, AnyType],
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
        retval: AnyType,
        task_id: str,
        args: tuple[AnyType, ...],
        kwargs: dict[str, AnyType],
    ) -> None:
        """Execute ação ao finalizar a task com sucesso.

        Args:
            retval (AnyType): Valor de retorno.
            task_id (str): Id da task.
            args (Tuple): Argumentos originais.
            kwargs (Dict): Argumentos nomeados originais.

        """
        ...

    def on_retry(
        self,
        exc: Exception,
        task_id: str,
        args: tuple[AnyType, ...],
        kwargs: dict[str, AnyType],
        einfo: AnyType,
    ) -> None:
        """Execute ação ao tentar novamente a task.

        Args:
            exc (Exception): Exceção de retry.
            task_id (str): Id da task.
            args (Tuple): Argumentos originais.
            kwargs (Dict): Argumentos nomeados originais.
            einfo (AnyType): Informações da exceção.

        """
        ...

    def on_failure(
        self,
        exc: Exception,
        task_id: str,
        args: tuple[AnyType, ...],
        kwargs: dict[str, AnyType],
        einfo: AnyType,
    ) -> None:
        """Execute ação ao falhar a task.

        Args:
            exc (Exception): Exceção lançada.
            task_id (str): Id da task.
            args (Tuple): Argumentos originais.
            kwargs (Dict): Argumentos nomeados originais.
            einfo (AnyType): Informações da exceção.

        """
        ...

    def after_return(
        self,
        status: str,
        retval: AnyType,
        task_id: str,
        args: tuple[AnyType, ...],
        kwargs: dict[str, AnyType],
        einfo: AnyType,
    ) -> None:
        """Execute ação após o retorno da task.

        Args:
            status (str): Estado atual.
            retval (AnyType): Valor/erro retornado.
            task_id (str): Id da task.
            args (Tuple): Argumentos originais.
            kwargs (Dict): Argumentos nomeados originais.
            einfo (AnyType): Informações da exceção.

        """
        ...

    def on_replace(self, sig: AnyType) -> None:
        """Execute ação ao substituir a task."""
        ...

    def add_trail(self, result: AnyType) -> None:
        """Adicione resultado ao trail da task."""
        ...

    def push_request(self, *args: AnyType, **kwargs: AnyType) -> None:
        """Empilhe uma nova requisição para a task."""
        ...

    def pop_request(self) -> AnyType:
        """Remova a requisição do topo da pilha."""
        ...

    def _get_request(self) -> AnyType:
        """Obtenha a requisição atual da task."""
        ...

    def _get_exec_options(self) -> AnyType:
        """Obtenha opções de execução da task."""
        ...

    @property
    def backend(self) -> AnyType:
        """Obtenha o backend da task."""
        ...

    @backend.setter
    def backend(self, value: AnyType) -> None:
        """Defina o backend da task."""
        ...
