# resources/driver/__init__.py

## Propósito

Gerenciador do webdriver para a execução dos bots.

## Dependências Principais

- `__future__`
- `backend.controllers.head`
- `backend.task_manager.constants`
- `backend.task_manager.constants.webdriver`
- `selenium.webdriver`
- `selenium.webdriver.chrome.options`
- `selenium.webdriver.support.wait`
- `typing`
- `webdriver_manager.chrome`
- `webdriver_manager.core.driver_cache`

## Classe: `BotDriver`

Gerenciador do webdriver para a execução dos bots.

### Métodos

#### `__init__()`

Inicialize o driver do bot com as configurações do sistema.

Args:
    bot (CrawJUD): Instância do controlador do bot.

**Parâmetros:**

- `self` (Any)
- `bot` (CrawJUD)

