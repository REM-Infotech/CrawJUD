# resources/search/main.py

## Propósito

Gerencie operações de busca automatizada usando Selenium.

Este módulo define a classe SearchBot para integrar
operações de busca com o bot principal CrawJUD.

## Dependências Principais

- `__future__`
- `backend.controllers.head`
- `backend.interfaces`
- `backend.resources.queues.print_message`
- `backend.types_app`
- `selenium.webdriver.chrome.webdriver`
- `selenium.webdriver.support.wait`
- `seleniumwire.webdriver`
- `typing`

## Classe: `SearchBot`

Gerencie operações de busca automatizada com Selenium.

Args:
    bot (CrawJUD): Instância do bot principal.

### Métodos

#### `__init__()`

Inicialize SearchBot com instância do bot principal.

Args:
    bot (CrawJUD): Instância do bot principal.

**Parâmetros:**

- `self` (Any)
- `bot` (CrawJUD)

#### `driver()`

Obtenha o driver Selenium do bot principal.

**Parâmetros:**

- `self` (Any)

**Retorna:** WebDriver | Chrome

#### `wait()`

Retorne o objeto de espera do Selenium do bot principal.

**Parâmetros:**

- `self` (Any)

**Retorna:** WebDriverWait[WebDriver | Chrome]

#### `print_message()`

Obtenha o gerenciador de mensagens do bot principal.

**Parâmetros:**

- `self` (Any)

**Retorna:** PrintMessage

#### `bot_data()`

Retorne os dados do bot principal.

**Parâmetros:**

- `self` (Any)

**Retorna:** BotData

#### `config()`

Retorne as configurações do bot principal.

**Parâmetros:**

- `self` (Any)

**Retorna:** Dict

