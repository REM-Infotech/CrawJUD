# resources/queues/print_message.py

## Propósito

Sistema de envio de logs para o ClientUI.

## Dependências Principais

- `backend.config`
- `backend.types_app`
- `clear`
- `contextlib`
- `datetime`
- `pathlib`
- `queue`
- `socketio.exceptions`
- `sys`
- `threading`

## Constantes

- `MSG_ROBO_INICIADO`
- `MSG_FIM_EXECUCAO`
- `MSG_ARQUIVO_BAIXADO`
- `MSG_EXECUCAO_SUCESSO`

## Classe: `Count`

Dicionario de contagem.

**Herda de:** `TypedDict`

### Atributos

- `sucessos` (int)
- `remainign_count` (int)
- `erros` (int)

## Classe: `PrintMessage`

Envio de logs para o FrontEnd.

### Atributos

- `bot` (CrawJUD)
- `_message_type` (MessageType)

### Métodos

#### `file_log()`

Retorne o caminho do arquivo de log do robô.

Returns:
    Path: Caminho do arquivo de log.

**Parâmetros:**

- `self` (Any)

**Retorna:** Path

#### `__init__()`

Instancia da queue de salvamento de sucessos.

**Parâmetros:**

- `self` (Any)
- `bot` (CrawJUD)

#### `__call__()`

Envie mensagem formatada para a fila de logs.

Args:
    message (str): Mensagem a ser enviada.
    message_type (MessageType): Tipo da mensagem.
    row (int): Linha do registro.
    link (str): Link do resultado (apenas no fim da execução)

**Parâmetros:**

- `self` (Any)
- `message` (MessageStr)
- `message_type` (MessageType)
- `row` (int)
- `link` (str | None)

#### `calc_success()`

Calcula o total de mensagens de sucesso.

Args:
    message_type (MessageType): Tipo da mensagem.

Returns:
    int: Quantidade de mensagens de sucesso.

**Parâmetros:**

- `self` (Any)
- `message_type` (MessageType)

**Retorna:** int

#### `calc_error()`

Calcula o total de mensagens de erro.

Args:
    message_type (MessageType): Tipo da mensagem.

Returns:
    int: Quantidade de mensagens de erro.

**Parâmetros:**

- `self` (Any)
- `message_type` (MessageType)

**Retorna:** int

#### `calc_remaining()`

Calcula o total de registros restantes.

Args:
    message_type (MessageType): Tipo da mensagem.

Returns:
    int: Quantidade de registros restantes.

**Parâmetros:**

- `self` (Any)
- `message_type` (MessageType)

**Retorna:** int

#### `_call_set_event()`

**Parâmetros:**

- `self` (Any)

#### `print_msg()`

Envie mensagens de log para o servidor via socket.

Esta função conecta ao servidor socketio e envia mensagens
presentes na fila para o FrontEnd.

**Parâmetros:**

- `self` (Any)

#### `emit_message()`

**Parâmetros:**

- `self` (Any)
- `data` (Message)
- `sio` (Client)

#### `set_event()`

Evento de parada do robô.

Args:
    *args (AnyType): Argumentos posicionais.
    **kwargs (AnyType): Argumentos nomeados.

**Parâmetros:**

- `self` (Any)

