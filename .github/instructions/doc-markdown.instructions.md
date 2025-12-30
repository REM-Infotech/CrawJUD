---
applyTo: "docs/**/*.md"
---

# Diretrizes para escrita da documentação do projeto

## Objetivo

Estas diretrizes definem o padrão de escrita para a documentação do projeto. O objetivo é garantir que todo o material seja **claro, consistente, fácil de manter e compreensível** para qualquer pessoa que utilize ou contribua com o projeto.

## Diretrizes Gerais

- Escreva documentação **clara, direta e objetiva**.
- Priorize a **legibilidade** em vez de formalidade excessiva.
- Use **terminologia consistente** em todo o projeto.
- Evite ambiguidades e frases vagas.
- Sempre que aplicável, **inclua exemplos práticos**, especialmente exemplos de código.
- Documente **o que o sistema faz**, **como funciona** e **como deve ser usado**.
- Assuma que o leitor **não conhece o contexto interno do projeto**.

## Estilo e Tom

- Utilize um tom **profissional, técnico e acessível**.
- Escreva de forma **instrucional**, guiando o leitor quando necessário.
- Seja direto e objetivo.
- Evite linguagem subjetiva ou opinativa.

## Gramática e Linguagem

- Utilize **tempo verbal no presente**.

  - ✔️ O sistema valida os dados
  - ❌ O sistema validou os dados

- Prefira **afirmações factuais e comandos diretos**.  
  Evite termos como:

  - poderia
  - talvez
  - normalmente
  - em geral

- Use **voz ativa**, onde o sujeito executa a ação.

  - ✔️ O serviço retorna a resposta
  - ❌ A resposta é retornada pelo serviço

- Escreva sempre em **segunda pessoa (você)** para se comunicar diretamente com o leitor.
  - ✔️ Você deve configurar o arquivo
  - ❌ O usuário deve configurar o arquivo

## Diretrizes de Markdown

### Estrutura

- Utilize títulos e subtítulos (`#`, `##`, `###`) para organizar o conteúdo.
- Cada documento deve ter um **título principal claro e descritivo**.
- Organize o conteúdo de forma hierárquica e previsível.

### Listas

- Utilize listas para:
  - Passos de processos
  - Requisitos
  - Boas práticas
  - Pontos importantes
- Prefira listas curtas e objetivas.

### Código

- Utilize **blocos de código** para qualquer trecho técnico:
  - Comandos de terminal
  - Exemplos de configuração
  - Código-fonte
- Sempre especifique a linguagem do bloco de código.

Exemplo:

```bash
npm install
```

```python
def main():
    print("Hello, world")
```

### Links

- Inclua links para:
  - Documentação relacionada
  - Referências externas
  - Outros arquivos do projeto
- Use textos de link descritivos.
  - ✔️ Consulte a documentação de configuração
  - ❌ Clique aqui

## Boas Práticas de Documentação

- Atualize a documentação sempre que o comportamento do sistema mudar.
- Evite duplicar informações em múltiplos arquivos.
- Explique **o motivo das decisões técnicas** quando não forem óbvias.
- Mantenha exemplos atualizados e funcionais.
- Indique claramente quando algo for experimental ou possuir limitações.

## Consistência

- Use o mesmo padrão de escrita em todos os arquivos.
- Padronize nomes de arquivos, seções e termos técnicos.
- Siga estas diretrizes para qualquer conteúdo adicionado à pasta `docs/`.
