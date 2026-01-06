---
name: "gerar-descricao-pr"
description: "Geração de titulo e descrição em um arquivo .md para pull-requests."

tools:
  [
    "execute",
    "edit",
    "search/codebase",
    "search/fileSearch",
    "search/listDirectory",
    "search/usages",
    "web/githubRepo",
    "github.vscode-pull-request-github/copilotCodingAgent",
    "github.vscode-pull-request-github/issue_fetch",
    "github.vscode-pull-request-github/suggest-fix",
    "github.vscode-pull-request-github/searchSyntax",
    "github.vscode-pull-request-github/doSearch",
    "github.vscode-pull-request-github/renderIssues",
    "github.vscode-pull-request-github/activePullRequest",
    "github.vscode-pull-request-github/openPullRequest",
  ]
---

Instruções para geração de titulo e descrição de Pull requests.
Essas instruções são para edição de titulo e corpo de uma pull request ativa
Caso não tenha pull request ativa, verifique se o usuario passou alguma e use esta.

## 1. Context gathering and research:

1. Você vai gerar um markdown para ser salvo em `.pull-requests/gh-{numeropullrequest}_{tipo-de-alteracao}.pullrequest.md`. Caso o arquivo já exista, sobreescreva
2. Siga as instruções dentro de <pullrequest_style_guide> e qualquer outra que o usuário indicar.
3. Aplique o titulo e o corpo na pull request ativa

<pullrequest_style_guide>
Siga este template (**não inclua as orientações entre `{}`**):

```markdown
## {

---

## [GH-{numero_pullrequest}] {Tipo de alteração (bugfixes, refact, feature, etc) capitalizado} - Breve resumo (2–10 palavras)

---

}

## 📖 Descrição

{

Descreva de forma clara e objetiva o que este Pull Request faz.

Inclua:

- O objetivo principal da mudança
- O problema ou necessidade que motivou o PR
- O impacto esperado no sistema

}

## ✨ Tipo de Mudança

{Insira as caixas a seguir e marque o que se aplica

- [ ] Nova funcionalidade
- [ ] Correção de bug
- [ ] Refatoração
- [ ] Melhoria de performance
- [ ] Ajustes estruturais / organização de código
- [ ] Infraestrutura / configuração
- [ ] Documentação
- [ ] Outro (descrever abaixo)
      }

## 🧩 O que foi alterado

- {Texto descritivo com subtexto informando:
  - Mudanças relevantes de lógica
  - Novos padrões ou abstrações introduzidas
    }

## 🏗️ Impacto Técnico

{Descreva impactos técnicos relevantes:

- Mudanças na arquitetura ou estrutura do projeto
- Alterações em fluxos existentes
- Dependências afetadas
- Possíveis efeitos colaterais
  }

## ⚠️ Breaking Changes

{Insira as caixas a seguir e marque o que se aplica

- [ ] Não
- [ ] Sim (descrever abaixo)
      }

{Se houver breaking changes, explique:

- O que mudou
- Quem é impactado
- O que precisa ser ajustado
  }

{- Mandatório: Insira tag a seguir apenas se os arquivos da pasta teste/ forem alterados ou tiver arquivos novos.}
{

## 🧪 Testes e Validação

Descreva como as mudanças foram testadas:

- Testes automatizados
- Testes manuais
- Cenários validados

}

## 🧹 Manutenção e Qualidade

{Insira as caixas a seguir e marque o que se aplica}
{- [ ] Código morto removido}
{- [ ] Imports/arquivos desnecessários removidos}
{- [ ] Melhorias de legibilidade}
{- [ ] Tipagem ou validações aprimoradas}
{- [ ] Comentários ou documentação adicionados}

## 📚 Observações para Revisão

{Inclua qualquer contexto que ajude na revisão:

- Decisões técnicas importantes
- Pontos que merecem atenção especial
- Limitações conhecidas
  }

## 🚀 Próximos Passos (Opcional)

{Sugestões de melhorias futuras ou follow-ups relacionados a este PR.}
```

Ao atualizar pull requests, use o comando **gh**.

> **Disclaimer: verificar se o **Github CLI (gh) ** está instalado, Caso não esteja, Solicite ao usuario que instale e aguarde a confirmação para prosseguir.**

<pullrequest_style_guide/>
