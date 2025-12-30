---
agent: "agent"
model: GPT-4.1 (copilot)
description: "Gerar documentação da pasta"
name: "gerar-doc

tools: ['edit', 'search/codebase', 'search/fileSearch', 'search/listDirectory', 'search/usages', 'web/githubRepo']

---

Geração de markdown para a pasta informada.

Com base no arquivo \*_doc-markdown.instructions.md_:

- Crie a documentação da pasta referida
- Salve os arquivos dentro de _docs/_
- Mantenha a estrutura real do projeto

Regras:

- Crie arquivos Markdown descrevendo cada arquivo
- Salve os arquivos dentro da pasta `docs/<caminho_relativo_arquivo>`, mantendo a estrutura dos diretorios
  - **Exemplo**:
    > **Arquivo _app/app.vue_ >> Documentação _docs/app/app.vue.md_**

- Para cada arquivo, documente:
  - Propósito
  - Props
  - Eventos (se houver)
  - Exemplo de uso (se possível)

# Regras para arquivos _\*.py_:

- Ao criar exemplos, faça como o codeblock abaixo:

  > ```python
  > def soma(a: int, b: int) -> int:
  >   """
  >   Retorne a soma de dois inteiros.
  >
  >   Args:
  >     a (int): Primeiro número.
  >     b (int): Segundo número.
  >
  >   Returns:
  >     int: Resultado da soma.
  >   """
  >   return a + b
  > ```

- Use o \*_doc-python.instructions.md_ para gerar os exemplos

# Regras para arquivos [_\*.js_, _\*.*js_, _\*.ts_]:

- Ao criar exemplos, faça como o codeblock abaixo:

> ```js
> /**
>  * Converter texto para número.
>  *
>  * @param {string} valor - Texto de entrada.
>  * @returns {number} Número convertido.
>  */
> function parse(valor) {
>   return Number(valor);
> }
> ```

- Use o \*_doc-javascript.instructions.md_ para gerar os exemplos
