---
name: analisar-linting
description: Analisar estado de liting de arquivos usando o ruff
argument-hint: "#<file> ou #codebase"

tools:
  ['execute', 'read', 'edit', 'search/codebase', 'search/fileSearch', 'search/listDirectory', 'search/usages', 'web/githubRepo']
---

Obrigatório: Antes de começar, ative o environment (.venv) do projeto.
Com base na pasta/arquivo/codebase, execute o ruff usando o ruff.toml do projeto.
Caso haja erros, liste indicando o arquivo, o erro e a referencia


Salve uma copia da listagem em ./erros_ruff/{hora.minuto.dia-mes-ano.md}

""