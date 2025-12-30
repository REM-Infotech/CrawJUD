# resources/auth/main.py

## Propósito

Gerencie autenticação e recursos relacionados a bots.

Este módulo fornece a classe AutenticadorBot para facilitar
operações de autenticação e acesso a recursos do bot.

## Dependências Principais

- `__future__`
- `backend.controllers.head`
- `backend.resources.managers.credencial_manager`
- `backend.resources.queues.print_message`
- `selenium.webdriver.chrome.webdriver`
- `selenium.webdriver.support.wait`
- `seleniumwire.webdriver`
- `typing`

## Classe: `AutenticadorBot`

Gerencie autenticação de bots no sistema.

Args:
    bot (CrawJUD): Instância do bot principal.

### Métodos

#### `__init__()`

Inicialize o autenticador com uma instância do bot.

Args:
    bot (CrawJUD): Instância do bot principal.

**Parâmetros:**

- `self` (Any)
- `bot` (CrawJUD)

#### `driver()`

Retorne o driver do bot para automação web.

**Parâmetros:**

- `self` (Any)

**Retorna:** WebDriver | Chrome

#### `wait()`

Obtenha o objeto de espera do driver do bot.

**Parâmetros:**

- `self` (Any)

**Retorna:** WebDriverWait[WebDriver | Chrome]

#### `print_message()`

Obtenha o gerenciador de mensagens do bot.

**Parâmetros:**

- `self` (Any)

**Retorna:** PrintMessage

#### `bot_data()`

Retorne os dados do bot para uso interno.

**Parâmetros:**

- `self` (Any)

**Retorna:** T

#### `credenciais()`

Obtenha o gerenciador de credenciais do bot.

**Parâmetros:**

- `self` (Any)

**Retorna:** CredencialManager

