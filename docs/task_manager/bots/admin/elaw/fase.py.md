# task_manager/bots/admin/elaw/fase.py

## Propósito

Gerencie atualização de fases processuais no sistema ELAW.

## Dependências Principais

- `__future__`
- `backend.common`
- `backend.controllers.elaw`
- `backend.resources.driver.web_element`
- `backend.resources.elements.elaw`
- `selenium.webdriver.common.by`
- `selenium.webdriver.support`
- `time`
- `traceback`
- `typing`

## Classe: `AtualizaFase`

Gerencie atualização de fase de fases no ELAW.

Esta classe executa a busca, atualização e confirmação
de fases processuais conforme parâmetros definidos.

**Herda de:** `ElawBot`

### Atributos

- `name` (ClassVar[str])

### Métodos

#### `execution()`

Execute atualização das fases processuais do ELAW.

Percorra o frame, atualize e processe cada linha.

**Parâmetros:**

- `self` (Any)

#### `queue()`

Execute busca e atualização de fase processual.

Tenta localizar o processo e atualizar sua fase;
registra erro caso não encontre ou ocorra falha.

**Parâmetros:**

- `self` (Any)

#### `atualizar()`

Atualiza fase processual do processo no sistema ELAW.

Busca e seleciona a nova fase e salva a alteração.

**Parâmetros:**

- `self` (Any)

#### `confirma_alteracao()`

Confirma alteração da fase e salve comprovante no ELAW.

Esta função verifica se a fase foi atualizada corretamente e
salva um comprovante em formato PNG na pasta de saída.

**Parâmetros:**

- `self` (Any)

