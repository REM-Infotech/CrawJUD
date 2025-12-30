# task_manager/bots/admin/jusds/prazos.py

## Propósito

Gerencie compromissos e prazos no sistema Jusds.

Fornece automação para criação e controle de compromissos
e prazos utilizando Selenium.

## Dependências Principais

- `backend.common.exceptions`
- `backend.resources.elements`
- `datetime`
- `master`
- `selenium.webdriver.common.by`
- `selenium.webdriver.support`
- `selenium.webdriver.support.wait`
- `time`
- `zoneinfo`

## Classe: `Prazos`

Gerencie compromissos e prazos no sistema Jusds.

Esta classe executa operações automatizadas para criar e
gerenciar compromissos e prazos utilizando Selenium.

**Herda de:** `JusdsBot`

### Métodos

#### `execution()`

Execute o processamento de cada linha do frame.

Itera sobre os dados do frame, atualizando o estado
interno para cada linha e finaliza a execução ao término.

**Parâmetros:**

- `self` (Any)

#### `queue()`

Processa a fila de criação de compromissos e trate exceções.

**Parâmetros:**

- `self` (Any)

#### `acesso_compromissos()`

Acesse a aba de compromissos no sistema Jusds.

**Parâmetros:**

- `self` (Any)

#### `criar_compromisso()`

Crie um novo compromisso na aba de compromissos do Jusds.

Preenche os campos obrigatórios do compromisso com dados do bot
e realiza o salvamento utilizando Selenium.

**Parâmetros:**

- `self` (Any)

#### `confirma_salvamento()`

Verifique se o compromisso foi salvo corretamente.

Returns:
    bool: True se o compromisso foi salvo, False caso contrário.

**Parâmetros:**

- `self` (Any)

**Retorna:** bool

