# task_manager/bots/admin/csi/download_documento.py

## Propósito

Download de anexos de chamados do CSI.

## Dependências Principais

- `__future__`
- `backend.controllers.csi`
- `backend.resources.driver.web_element`
- `backend.resources.elements`
- `contextlib`
- `dotenv`
- `httpx`
- `selenium.webdriver.support`
- `selenium.webdriver.support.wait`
- `typing`

## Classe: `DownloadDocumento`

Robô de download de documentos do CSI.

**Herda de:** `CsiBot`

### Métodos

#### `execution()`

Execute o processamento dos chamados e baixe os anexos.

Args:
    *args (AnyType): Argumentos posicionais.
    **kwargs (AnyType): Argumentos nomeados.

**Parâmetros:**

- `self` (Any)

#### `queue()`

Processa o chamado atual e baixe seus anexos.

Esta função busca o chamado, imprime mensagens de status e
realiza o download dos anexos. Em caso de erro, registra o motivo.

**Parâmetros:**

- `self` (Any)

#### `busca_chamado()`

Busque o chamado pelo número informado e retorne o elemento.

Returns:
    WebElement: Elemento da tabela de solicitações encontrado.

**Parâmetros:**

- `self` (Any)

**Retorna:** WebElement

#### `download_anexos_chamado()`

Baixe todos os anexos do chamado atual do CSI.

**Parâmetros:**

- `self` (Any)

#### `swtich_iframe_anexos()`

Troque para o iframe de anexos do chamado no CSI.

Args:
    wait (WebDriverWait): Objeto de espera do Selenium.

**Parâmetros:**

- `self` (Any)
- `wait` (WebDriverWait)

