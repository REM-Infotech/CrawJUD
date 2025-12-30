# task_manager/bots/admin/csi/chamados.py

## Propósito

Gerencia tarefas e execução de chamados CSI para automação judicial.

Este módulo define a classe Chamados, responsável por orquestrar tarefas
automatizadas relacionadas a chamados CSI, utilizando integração com bots,
tratamento de contexto e execução assíncrona de tarefas.

## Dependências Principais

- `backend.controllers.csi`
- `backend.resources.elements`
- `dotenv`
- `selenium.webdriver.common.by`
- `selenium.webdriver.support`
- `selenium.webdriver.support.wait`
- `time`
- `tqdm`

## Classe: `Chamados`

Gerencia chamados CSI para execução de tarefas automatizadas.

Herda de CsiBot e implementa métodos de execução de chamados.

**Herda de:** `CsiBot`

### Métodos

#### `execution()`

Execute os chamados CSI conforme o quadro de tarefas.

Este método percorre o frame de tarefas e executa
a função correspondente para cada chamado CSI.

**Parâmetros:**

- `self` (Any)

#### `solicita_subsid()`

Solicite subsídios para contestação no sistema CSI.

Este método preenche e envia o formulário de solicitação
de subsídios para contestação, utilizando dados do chamado.

**Parâmetros:**

- `self` (Any)

