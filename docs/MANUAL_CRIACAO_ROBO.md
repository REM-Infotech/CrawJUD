# Manual: Como Criar um Robô no CrawJUD

Este manual orienta você a criar um novo robô de automação judicial no projeto CrawJUD, seguindo as boas práticas e padrões do repositório.

## 1. Planeje o Robô

- Defina o objetivo do robô (ex: buscar processos, emitir documentos, protocolar petições).
- Identifique o tribunal ou sistema alvo (PJE, ESAJ, Projudi, etc).
- Liste os requisitos funcionais e dados necessários.

## 2. Estruture o Código

- Crie o arquivo do robô em `backend/task_manager/bots/<categoria>/<tribunal>/`.
  - Exemplo: `backend/task_manager/bots/capa/pje.py`
- Utilize o nome do arquivo e da classe de forma descritiva.
- Importe e herde do controller correspondente em `backend/controllers/<tribunal>.py`.
- Siga o padrão de estrutura dos robôs do projeto:
  - Classe principal herda do controller (ex: `PJeBot`, `ESajBot`, `ProjudiBot`, `JusdsBot`).
  - Métodos principais: `execution(self)`, `queue(self)`, métodos auxiliares privados (`_extrair_dados`, `_autenticar`, etc).
  - Utilize atributos como `self.frame`, `self.row`, `self.bot_data` para iterar e processar dados.

```python
from backend.controllers.pje import PJeBot

class CapaPJE(PJeBot):
    """
    Implemente a extração da capa do processo no PJE.
    Args:
        ...
    Returns:
        ...
    """
    def execution(self) -> None:
        frame = self.frame
        for pos, item in enumerate(frame):
            self.row = pos + 1
            self.bot_data = item
            try:
                self.queue()
            except Exception as e:
                self.print_message(str(e), "error", self.row)
        self.finalizar_execucao()

    def queue(self) -> None:
        # Lógica do robô
        pass
```

## 3. Implemente a Lógica

- Use os recursos de automação do Selenium disponíveis em `backend/resources/driver/`.
- Utilize elementos e locators de `backend/resources/elements/<tribunal>.py`.
- Utilize BeautifulSoup para parsing de HTML quando necessário.
- Siga o padrão de docstring do projeto (ver exemplos abaixo).
- Adicione tipagem explícita em todos os métodos e parâmetros.
- Utilize tratamento de erros com `try/except` e classes de exceção do projeto (`ExecutionError`, etc).
- Use `self.print_message` para logs e feedback em tempo real.
- Aguarde elementos com `self.wait.until(...)` antes de interagir.
- Implemente métodos privados para etapas específicas.

## 4. Defina a Task Celery

- Crie a task correspondente em `backend/task_manager/tasks/`.
- Registre a task no Celery para execução assíncrona.

## 5. Teste Manualmente

- Execute o robô via CLI ou Celery para validar o funcionamento.
- Corrija eventuais erros e revise docstrings e comentários.

## 6. Documente o Robô

- Adicione exemplos de uso e instruções de configuração, se necessário.
- Atualize a documentação caso o robô dependa de credenciais, certificados ou configurações específicas.

## Exemplo Avançado de Estrutura de Robô

```python
from backend.controllers.projudi import ProjudiBot

class MovimentacaoProjudi(ProjudiBot):
    """
    Raspagem de movimentações no Projudi.
    Args:
        processo_id (str): Identificador do processo.
    Returns:
        dict: Dados das movimentações extraídas.
    """
    def execution(self) -> None:
        frame = self.frame
        for pos, item in enumerate(frame):
            self.row = pos + 1
            self.bot_data = item
            try:
                self.queue()
            except Exception as e:
                self.print_message(str(e), "error", self.row)
        self.finalizar_execucao()

    def queue(self) -> None:
        # Aguarde elemento, busque dados, trate erros
        self.print_message(f"Buscando processo {self.bot_data['NUMERO_PROCESSO']}", "log")
        search = self.search()
        if not search:
            self.print_message("Processo não encontrado!", "error")
            return
        self.set_page_size()
        self.extrair_movimentacoes()
```

## Boas Práticas

- Siga o padrão de docstring e tipagem obrigatória.
- Utilize comentários explicativos para trechos complexos.
- Mantenha o código modular e reutilizável.
- Separe métodos para cada etapa do fluxo.
- Utilize `ClassVar` para atributos estáticos quando necessário.
- Atualize a documentação sempre que alterar o comportamento do robô.

## Dicas Avançadas

- Implemente métodos privados para etapas específicas (`_extrair_dados`, `_autenticar`, etc).
- Use `contextlib.suppress` para ignorar exceções pontuais.
- Utilize BeautifulSoup para parsing de tabelas HTML.
- Para robôs multi-instância (primeira/segunda), crie subclasses separadas.
- Utilize recursos de scraping e manipulação de arquivos conforme necessário.

## Referências

- [Exemplo de Movimentação Projudi](../backend/task_manager/bots/movimentacao/projudi/__init__.py)
- [Exemplo de Provisionamento Jusds](../backend/task_manager/bots/provisionamento/jusds.py)
- [Padrão de Docstring Python](../.github/instructions/doc-python.instructions.md)
- [Diretrizes de Markdown](../.github/instructions/doc-markdown.instructions.md)
- [Estrutura do Projeto](PROJECT_STRUCTURE.md)

---

Você está pronto para criar um novo robô no CrawJUD!
