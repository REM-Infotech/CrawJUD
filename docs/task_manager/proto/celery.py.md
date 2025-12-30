# task_manager/proto/celery.py

## Propósito

Módulo de controle de protocolos.

## Dependências Principais

- `__future__`
- `backend.types_app`
- `celery`
- `typing`

## Classe: `CeleryTask`

Defina o protocolo para tasks Celery genéricas.

**Herda de:** `Protocol[P, T]`

### Métodos

#### `bind()`

Vincule a task ao app Celery.

**Parâmetros:**

- `cls` (Any)
- `app` (Celery)

#### `on_bound()`

Execute ações adicionais ao vincular a task ao app.

**Parâmetros:**

- `cls` (Any)
- `app` (Celery)

#### `_get_app()`

Obtenha a instância do app Celery.

**Parâmetros:**

- `cls` (Any)

#### `annotate()`

Anote a task com metadados adicionais.

**Parâmetros:**

- `cls` (Any)

#### `add_around()`

Adicione lógica ao redor de um atributo da task.

**Parâmetros:**

- `cls` (Any)
- `attr` (str)
- `around` (AnyType)

#### `run()`

Execute o corpo da task Celery.

**Parâmetros:**

- `self` (Any)

#### `start_strategy()`

Inicie a estratégia de execução da task.

**Parâmetros:**

- `self` (Any)
- `app` (AnyType)
- `consumer` (AnyType)

#### `delay()`

Execute a task de forma assíncrona (atalho para apply_async).

Retorna:
    AsyncResult: Resultado futuro da execução.

**Parâmetros:**

- `self` (Any)

**Retorna:** AnyType

#### `apply_async()`

Agende a execução assíncrona da task.

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

**Parâmetros:**

- `self` (Any)

**Retorna:** AnyType

#### `shadow_name()`

Retorne nome customizado da task para logs/monitoramento.

**Parâmetros:**

- `self` (Any)
- `args` (tuple[AnyType, ...])
- `kwargs` (dict[str, AnyType])
- `options` (dict[str, AnyType])

**Retorna:** AnyType

#### `retry()`

Reagende a execução da task para nova tentativa.

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

**Parâmetros:**

- `self` (Any)

#### `apply()`

Execute a task localmente e bloqueie até o retorno.

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

**Parâmetros:**

- `self` (Any)

**Retorna:** AnyType

#### `AsyncResult()`

Obtenha AsyncResult para o id da tarefa especificada.

Args:
    task_id (str): Id da tarefa para obter o resultado.
    **kwargs: Argumentos adicionais para configuração.

**Parâmetros:**

- `self` (Any)
- `task_id` (str)

#### `signature()`

Crie uma assinatura para a task.

**Parâmetros:**

- `self` (Any)
- `args` (tuple[AnyType, ...] | None)

#### `s()`

Crie uma assinatura para a task (atalho).

**Parâmetros:**

- `self` (Any)

#### `si()`

Crie assinatura imutável para a task.

**Parâmetros:**

- `self` (Any)

#### `chunks()`

Crie task de chunks para processamento em lotes.

**Parâmetros:**

- `self` (Any)
- `it` (AnyType)
- `n` (int)

**Retorna:** AnyType

#### `map()`

Crie task de map para processamento iterativo.

**Parâmetros:**

- `self` (Any)
- `it` (AnyType)

**Retorna:** AnyType

#### `starmap()`

Crie task de starmap para processamento iterativo.

**Parâmetros:**

- `self` (Any)
- `it` (AnyType)

**Retorna:** AnyType

#### `send_event()`

Envie evento de monitoramento customizado.

Args:
    type_ (str): Tipo do evento.
    retry (bool, opcional): Tentar novamente em falha.
    retry_policy (AnyType, opcional): Política de retry.
    **fields: Campos adicionais do evento.

**Parâmetros:**

- `self` (Any)

#### `replace()`

Substitua esta task por outra mantendo o mesmo id.

Args:
    sig (AnyType): Assinatura substituta.

**Parâmetros:**

- `self` (Any)
- `sig` (AnyType)

#### `add_to_chord()`

Adicione assinatura ao chord da task.

Args:
    sig (AnyType): Assinatura a adicionar.
    lazy (bool, opcional): Não executar imediatamente.

**Parâmetros:**

- `self` (Any)
- `sig` (AnyType)

#### `update_state()`

Atualize o estado da task.

Args:
    task_id (str, opcional): Id da task.
    state (str, opcional): Novo estado.
    meta (Dict, opcional): Metadados do estado.
    **kwargs: Argumentos adicionais.

**Parâmetros:**

- `self` (Any)
- `task_id` (str | None)
- `state` (str | None)
- `meta` (dict[str, AnyType] | None)

#### `before_start()`

Execute ação antes de iniciar a task.

Args:
    task_id (str): Id da task.
    args (Tuple): Argumentos originais.
    kwargs (Dict): Argumentos nomeados originais.

**Parâmetros:**

- `self` (Any)
- `task_id` (str)
- `args` (tuple[AnyType, ...])
- `kwargs` (dict[str, AnyType])

#### `on_success()`

Execute ação ao finalizar a task com sucesso.

Args:
    retval (AnyType): Valor de retorno.
    task_id (str): Id da task.
    args (Tuple): Argumentos originais.
    kwargs (Dict): Argumentos nomeados originais.

**Parâmetros:**

- `self` (Any)
- `retval` (AnyType)
- `task_id` (str)
- `args` (tuple[AnyType, ...])
- `kwargs` (dict[str, AnyType])

#### `on_retry()`

Execute ação ao tentar novamente a task.

Args:
    exc (Exception): Exceção de retry.
    task_id (str): Id da task.
    args (Tuple): Argumentos originais.
    kwargs (Dict): Argumentos nomeados originais.
    einfo (AnyType): Informações da exceção.

**Parâmetros:**

- `self` (Any)
- `exc` (Exception)
- `task_id` (str)
- `args` (tuple[AnyType, ...])
- `kwargs` (dict[str, AnyType])
- `einfo` (AnyType)

#### `on_failure()`

Execute ação ao falhar a task.

Args:
    exc (Exception): Exceção lançada.
    task_id (str): Id da task.
    args (Tuple): Argumentos originais.
    kwargs (Dict): Argumentos nomeados originais.
    einfo (AnyType): Informações da exceção.

**Parâmetros:**

- `self` (Any)
- `exc` (Exception)
- `task_id` (str)
- `args` (tuple[AnyType, ...])
- `kwargs` (dict[str, AnyType])
- `einfo` (AnyType)

#### `after_return()`

Execute ação após o retorno da task.

Args:
    status (str): Estado atual.
    retval (AnyType): Valor/erro retornado.
    task_id (str): Id da task.
    args (Tuple): Argumentos originais.
    kwargs (Dict): Argumentos nomeados originais.
    einfo (AnyType): Informações da exceção.

**Parâmetros:**

- `self` (Any)
- `status` (str)
- `retval` (AnyType)
- `task_id` (str)
- `args` (tuple[AnyType, ...])
- `kwargs` (dict[str, AnyType])
- `einfo` (AnyType)

#### `on_replace()`

Execute ação ao substituir a task.

**Parâmetros:**

- `self` (Any)
- `sig` (AnyType)

#### `add_trail()`

Adicione resultado ao trail da task.

**Parâmetros:**

- `self` (Any)
- `result` (AnyType)

#### `push_request()`

Empilhe uma nova requisição para a task.

**Parâmetros:**

- `self` (Any)

#### `pop_request()`

Remova a requisição do topo da pilha.

**Parâmetros:**

- `self` (Any)

**Retorna:** AnyType

#### `_get_request()`

Obtenha a requisição atual da task.

**Parâmetros:**

- `self` (Any)

**Retorna:** AnyType

#### `_get_exec_options()`

Obtenha opções de execução da task.

**Parâmetros:**

- `self` (Any)

**Retorna:** AnyType

#### `backend()`

Obtenha o backend da task.

**Parâmetros:**

- `self` (Any)

**Retorna:** AnyType

#### `backend()`

Defina o backend da task.

**Parâmetros:**

- `self` (Any)
- `value` (AnyType)

