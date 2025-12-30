# resources/driver/web_element.py

## Propósito

Module for managing WebDriver instances and related utilities.

## Dependências Principais

- `__future__`
- `backend.types_app`
- `pathlib`
- `selenium.webdriver.common.action_chains`
- `selenium.webdriver.common.actions.wheel_input`
- `selenium.webdriver.remote.command`
- `selenium.webdriver.remote.webelement`
- `selenium.webdriver.support.ui`
- `seleniumwire.webdriver`
- `typing`

## Classe: `RectWebElement`

Dict Rect Webelement.

**Herda de:** `TypedDict`

### Atributos

- `height` (float)
- `width` (float)
- `x` (float)
- `y` (float)

## Classe: `WebElement`

Gerencie e interaja com elementos web personalizados.

**Herda de:** `SEWebElement`

### Atributos

- `_current_driver` (WebDriver)
- `_action` (ActionChains)
- `parent` (WebDriver | Chrome)

### Métodos

#### `__call__()`

Execute um clique no elemento ao chamar a instância.

Args:
    *args (AnyType): Argumentos posicionais.
    **kwargs (AnyType): Argumentos nomeados.

**Parâmetros:**

- `self` (Any)

#### `set_driver()`

Defina o driver atual para a classe e inicialize ActionChains.

Args:
    _driver (WebDriver): Instância do driver a ser utilizada.

Returns:
    type[Self]: Classe atual com driver configurado.

**Parâmetros:**

- `cls` (Any)
- `_driver` (WebDriver)

**Retorna:** type[Self]

#### `rect()`

Obtenha o retângulo do elemento na página.

**Parâmetros:**

- `self` (Any)

**Retorna:** RectWebElement

#### `location()`

Obtenha a posição do elemento na página.

**Parâmetros:**

- `self` (Any)

**Retorna:** RectWebElement

#### `current_driver()`

Obtenha o driver atual associado ao elemento web.

**Parâmetros:**

- `self` (Any)

**Retorna:** WebDriver | Chrome

#### `double_click()`

Execute um duplo clique no elemento web.

**Parâmetros:**

- `self` (Any)

#### `select_item()`

Selecione um item em um elemento select pelo valor.

Args:
    item (str): Valor do item a ser selecionado.

**Parâmetros:**

- `self` (Any)
- `item` (str)

#### `click()`

Perform a click action on a web element with brief pauses.

Args:
    element (WebElement): The target web element.

Implements a click with pre- and post-click delays.

**Parâmetros:**

- `self` (Any)

#### `clear()`

Limpe o conteúdo do elemento web após clicar e aguardar.

**Parâmetros:**

- `self` (Any)

#### `scroll_to()`

Scroll the view to the specified web element.

**Parâmetros:**

- `self` (Any)

#### `find_element()`

Localize e retorne um elemento filho deste elemento.

Args:
    by (str): Estratégia de localização (ex: By.ID).
    value (AnyType | None): Valor a ser buscado.

Returns:
    WebElement: Elemento encontrado.

**Parâmetros:**

- `self` (Any)
- `by` (str)
- `value` (AnyType | None)

**Retorna:** WebElement

#### `find_elements()`

Localize e retorne uma lista de elementos filhos deste elemento.

Args:
    by (str): Estratégia de localização (ex: By.ID).
    value (AnyType | None): Valor a ser buscado.

Returns:
    list[WebElement]: Lista de elementos encontrados.

**Parâmetros:**

- `self` (Any)
- `by` (str)
- `value` (AnyType | None)

**Retorna:** list[WebElement]

#### `send_keys()`

Envie teclas ou texto para o elemento web.

Args:
    word (AnyType): Tecla ou texto a ser enviado.

**Parâmetros:**

- `self` (Any)
- `word` (AnyType)

#### `send_file()`

Envie um arquivo para o elemento input do tipo file.

Args:
    file (str | Path): Caminho do arquivo a ser enviado.

**Parâmetros:**

- `self` (Any)
- `file` (str | Path)

#### `display_none()`

Wait for an element's display style to change to 'none'.

Args:
    elemento (WebElement): The element to monitor.

**Parâmetros:**

- `self` (Any)

#### `select2()`

Select an option from a Select2 dropdown based on a search text.

Args:
    to_search (str): The option text to search and select.

**Parâmetros:**

- `self` (Any)
- `to_search` (str)

#### `scroll_from_origin()`

Role a partir de uma origem específica no elemento web.

Args:
    delta_x (int): Deslocamento horizontal.
    delta_y (int): Deslocamento vertical.
    origin (Self | None): Elemento de origem do scroll.

**Parâmetros:**

- `self` (Any)
- `delta_x` (int)
- `delta_y` (int)
- `origin` (Self | None)

#### `scroll_to_element()`

Scroll to element.

If the element is outside the viewport, scrolls the bottom of the
element to the bottom of the viewport.

Args:
    element: Which element to scroll into the viewport.

**Parâmetros:**

- `self` (Any)

#### `blur()`

Remova o foco do elemento web usando JavaScript.

Remove o foco do elemento utilizando o id, se existir,
ou o próprio elemento como fallback.

**Parâmetros:**

- `self` (Any)

