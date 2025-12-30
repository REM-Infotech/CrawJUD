# controllers/head.py

## Propósito

Implemente funcionalidades principais do bot CrawJUD.

## Dependências Principais

- `backend.resources.managers.credencial_manager`
- `backend.resources.queues.print_message`
- `backend.types_app`
- `clear`
- `contextlib`
- `datetime`
- `pathlib`
- `seleniumwire.webdriver`
- `threading`
- `warnings`

## Constantes

- `MODULE_SPLIT_SIZE`
- `TZ`
- `FORMAT_TIME`

## Classe: `CrawJUD`

Implemente a abstração do bot CrawJUD.

### Atributos

- `bots` (ClassVar[dict[str, type[Self]]])
- `row` (int)
- `_total_rows` (int)
- `remaining` (int)

### Métodos

#### `name()`

Retorne o nome do bot CrawJUD.

**Parâmetros:**

- `self` (Any)

**Retorna:** str

#### `shutdown_all()`

**Parâmetros:**

- `self` (Any)

#### `__subclasshook__()`

Registre subclasses do CrawJUD automaticamente.

**Parâmetros:**

- `cls` (Any)

#### `__init_subclass__()`

Inicialize subclasses do CrawJUD e registre bots.

Args:
    cls (type): Subclasse de CrawJUD.

**Parâmetros:**

- `cls` (Any)

#### `setup()`

Configure o bot com as opções fornecidas.

Args:
    config (Dict): Configurações do bot.

Returns:
    Self: Instância configurada do bot.

**Parâmetros:**

- `self` (Any)
- `config` (Dict)

**Retorna:** Self

#### `finalizar_execucao()`

Finalize a execução do bot e faça upload dos resultados.

**Parâmetros:**

- `self` (Any)

#### `execution()`

Execute as ações principais do bot.

Raises:
    NotImplementedError: Método deve ser implementado
        pelas subclasses.

**Parâmetros:**

- `self` (Any)

#### `auth()`

**Parâmetros:**

- `self` (Any)

#### `driver()`

Retorne o driver do navegador utilizado pelo bot.

**Parâmetros:**

- `self` (Any)

**Retorna:** WebDriver | Chrome

#### `wait()`

Retorne o objeto de espera do driver do navegador.

**Parâmetros:**

- `self` (Any)

**Retorna:** WebDriverWait[WebDriver | Chrome]

#### `output_dir_path()`

Retorne o caminho do diretório de saída do bot.

Returns:
    Path: Caminho do diretório de saída criado.

**Parâmetros:**

- `self` (Any)

**Retorna:** Path

#### `xlsx()`

Retorne o caminho da planilha XLSX utilizada pelo bot.

**Parâmetros:**

- `self` (Any)

**Retorna:** str

#### `xlsx()`

**Parâmetros:**

- `self` (Any)
- `val` (str)

#### `pid()`

Retorne o identificador do processo do bot.

Returns:
    str: Identificador do processo.

**Parâmetros:**

- `self` (Any)

**Retorna:** str

#### `anexos()`

Retorne a lista de anexos do bot.

Returns:
    list[str]: Lista de caminhos dos anexos.

**Parâmetros:**

- `self` (Any)

**Retorna:** list[str]

#### `total_rows()`

Retorne o total de linhas processadas pelo bot.

Returns:
    int: Número total de linhas.

**Parâmetros:**

- `self` (Any)

**Retorna:** int

#### `total_rows()`

**Parâmetros:**

- `self` (Any)
- `value` (int)

#### `now()`

Retorne a data e hora atual formatada.

Returns:
    str: Data e hora no formato 'dd-mm-YYYY HH-MM-SS'.

**Parâmetros:**

- `self` (Any)

**Retorna:** str

## Classe: `BotUtil`

### Métodos

#### `on_done()`

**Parâmetros:**

- `fut` (Future[None])

#### `create_thread_shutdown()`

**Parâmetros:**

- `bot` (CrawJUD)

#### `logging_fatal_error()`

**Parâmetros:**

- `e` (Exception)
- `bot` (CrawJUD)

**Retorna:** FatalError

## Função: `start_bot()`

Inicie o bot CrawJUD com a configuração fornecida.

Args:
    config (Dict): Configuração do bot.

Returns:
    None: Não retorna valor.

**Parâmetros:**

- `config` (Dict)

### Exemplo de Uso

```python
start_bot(config)
```

