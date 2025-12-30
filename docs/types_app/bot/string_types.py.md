# types_app/bot/string_types.py

## Propósito

Fornece tipos e utilitários para manipulação de strings.

## Dependências Principais

- `__future__`
- `backend.common.raises`
- `backend.task_manager.constants`
- `backend.types_app`
- `collections`
- `contextlib`
- `datetime`
- `re`
- `typing`
- `zoneinfo`

## Classe: `ProcessoCNJ`

Classe(str) ProcessoCNJ para processos no padrão CNJ.

**Herda de:** `UserString`

### Métodos

#### `__init__()`

Inicializa a classe StrTime.

**Parâmetros:**

- `self` (Any)
- `seq` (str)

#### `__validate_str()`

**Parâmetros:**

- `self` (Any)

**Retorna:** bool

#### `tj()`

Extrai o ID do TJ.

Returns:
    str: TJ ID

**Parâmetros:**

- `self` (Any)

**Retorna:** str

#### `__str__()`

Retorne a representação em string da instância StrTime.

Returns:
    str: Representação textual da instância.

**Parâmetros:**

- `self` (Any)

**Retorna:** str

#### `__instancecheck__()`

Verifique se a instância corresponde a padrões de string CNJ.

Args:
    instance: Instância a ser verificada.

Returns:
    bool: Indica se a instância corresponde a
        algum dos padrões de string CNJ.

**Parâmetros:**

- `self` (Any)
- `instance` (AnyType)

**Retorna:** bool

## Classe: `MessageLog`

Classe para manipular mensagens de log formatadas e tipadas.

Esta classe herda de UserString e permite formatar mensagens de log
com informações de identificação, tipo de mensagem, linha e horário
de execução, facilitando o rastreamento e auditoria de eventos.

**Herda de:** `UserString`

### Métodos

#### `format()`

Formata mensagem de log com PID, tipo, linha e horário.

Args:
    pid (str): Identificador do processo.
    message_type (MessageType): Tipo da mensagem.
    row (int): Linha do evento.

Returns:
    Self: Instância atual com mensagem formatada.

**Parâmetros:**

- `self` (Any)
- `pid` (str)
- `message_type` (MessageType)
- `row` (int)

**Retorna:** Self

