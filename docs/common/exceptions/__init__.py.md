# common/exceptions/__init__.py

## Propósito

Módulo de tratamento de exceptions do robô.

## Dependências Principais

- `__future__`
- `traceback`
- `typing`

## Classe: `BaseCrawJUDError`

Base exception class for CrawJUD-specific errors.

Fornece formatação automática de mensagens de erro e
integração com exceções aninhadas.

**Herda de:** `Exception`

### Métodos

#### `__init__()`

Inicialize a exceção com mensagem e exceção opcional.

Args:
    message (str): Mensagem de erro principal.
    exc (Exception | None): Exceção original, se houver.

**Parâmetros:**

- `self` (Any)
- `message` (str)
- `exc` (Exception | None)

#### `__str__()`

Retorne a mensagem de erro formatada.

Returns:
    str: Mensagem de erro com detalhes da exceção.

**Parâmetros:**

- `self` (Any)

**Retorna:** str

## Classe: `StartError`

Exception raised for errors that occur during the start of the bot.

**Herda de:** `BaseCrawJUDError`

## Classe: `DriverNotCreatedError`

Handler de erro de inicialização do WebDriver.

**Herda de:** `BaseCrawJUDError`

## Classe: `AuthenticationError`

Handler de erro de autenticação.

**Herda de:** `BaseCrawJUDError`

### Métodos

#### `__init__()`

Inicializa a mensagem de erro.

**Parâmetros:**

- `self` (Any)
- `message` (str)

## Classe: `BaseExceptionCeleryAppError`

Base exception class for Celery app errors.

**Herda de:** `Exception`

## Classe: `BotNotFoundError`

Exceção para indicar que o robô especificado não foi encontrado.

Args:
    message (str): Mensagem de erro.

Returns:
    None

Raises:
    AttributeError: Sempre que o robô não for localizado.

**Herda de:** `AttributeError`

### Métodos

#### `__init__()`

Inicializa a exceção BotNotFoundError.

Args:
    message (str): Mensagem de erro.
    name (str | None): Nome do robô, se disponível.
    obj (object | None): Objeto relacionado ao erro, se disponível.

**Parâmetros:**

- `self` (Any)
- `message` (str)
- `name` (str | None)
- `obj` (object | None)

## Classe: `ExecutionError`

Exceção para erros de execução do robô.

**Herda de:** `BaseCrawJUDError`

### Métodos

#### `__init__()`

Inicialize exceção de execução com formatação especial.

Args:
    message (str): Mensagem de erro principal.
    exc (Exception | None): Exceção original capturada.

**Parâmetros:**

- `self` (Any)
- `message` (str)
- `exc` (Exception | None)

## Classe: `LoginSystemError`

Exceção para erros de login robô.

**Herda de:** `BaseCrawJUDError`

## Classe: `ProcNotFoundError`

Exception de Processo não encontrado.

**Herda de:** `BaseCrawJUDError`

## Classe: `GrauIncorretoError`

Exception de Grau Incorreto/Não informado.

**Herda de:** `BaseCrawJUDError`

## Classe: `SaveError`

Exception para erros de salvamento de Formulários/Arquivos.

**Herda de:** `BaseCrawJUDError`

## Classe: `FileError`

Exception para erros de envio de arquivos.

**Herda de:** `BaseCrawJUDError`

## Classe: `CadastroParteError`

Exception para erros de cadastro de parte no Elaw.

**Herda de:** `BaseCrawJUDError`

## Classe: `MoveNotFoundError`

Exception para erros de movimentações não encontradas.

**Herda de:** `BaseCrawJUDError`

## Classe: `PasswordError`

Exception para erros de senha.

**Herda de:** `BaseCrawJUDError`

## Classe: `NotFoundError`

Exceção para erros de execução do robô.

**Herda de:** `BaseCrawJUDError`

## Classe: `FileUploadError`

Exception para erros de upload de arquivos.

**Herda de:** `BaseCrawJUDError`

## Classe: `PasswordTokenError`

Handler de erro de senha de token Projudi.

**Herda de:** `BaseCrawJUDError`

### Atributos

- `message` (ClassVar[str])

### Métodos

#### `__init__()`

Inicializa a mensagem de erro.

**Parâmetros:**

- `self` (Any)
- `message` (MessageTokenError)

## Função: `formata_msg()`

Formata mensagem de erro detalhada a partir de uma exceção fornecida ao bot.

Args:
    exc (Exception | None): Exceção a ser formatada, se fornecida.

Returns:
    str: Mensagem formatada contendo detalhes da exceção, se houver.

**Parâmetros:**

- `exc` (Exception | None)

**Retorna:** str

### Exemplo de Uso

```python
resultado = formata_msg(exc)
```

## Função: `raise_start_error()`

Lança exceção StartError com mensagem personalizada fornecida.

Args:
    message (str): Mensagem de erro a ser exibida na exceção.

Raises:
    StartError: Exceção lançada com a mensagem informada.

**Parâmetros:**

- `message` (str)

**Retorna:** NoReturn

### Exemplo de Uso

```python
resultado = raise_start_error(message)
```

