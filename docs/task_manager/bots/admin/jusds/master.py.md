# task_manager/bots/admin/jusds/master.py

## Propósito

Módulo para a classe de controle dos robôs Jusds.

## Dependências Principais

- `backend.controllers.head`
- `backend.interfaces`
- `backend.resources.elements`
- `contextlib`
- `selenium.webdriver.common.by`
- `selenium.webdriver.support`
- `selenium.webdriver.support.ui`
- `selenium.webdriver.support.wait`

## Classe: `JusdsBot`

Classe de controle para robôs do Jusds.

**Herda de:** `CrawJUD`

### Métodos

#### `auth()`

Realize a autenticação no sistema Jusds.

Returns:
    bool: Indica se a autenticação foi bem-sucedida.

**Parâmetros:**

- `self` (Any)

**Retorna:** bool

#### `search()`

Busca processos no JUSDS.

Returns:
    bool: Boleano da busca processual

**Parâmetros:**

- `self` (Any)

**Retorna:** bool

#### `print_comprovante()`

Salve comprovante do processo e registre mensagem de sucesso.

Args:
    message (str): Mensagem a ser exibida no comprovante.

**Parâmetros:**

- `self` (Any)
- `message` (str)

#### `exit_iframe()`

Saia do iframe e atualize ou navegue para o link correto.

**Parâmetros:**

- `self` (Any)

