---
## [GH-23] feature - Integração inicial de branch devel
---

## 📖 Descrição

Este Pull Request realiza a integração inicial da branch devel na main.

- Objetivo: Unificar as alterações acumuladas na branch de desenvolvimento.
- Motivação: Sincronizar novas funcionalidades, correções e melhorias estruturais do backend CrawJUD.
- Impacto: Atualização significativa do backend, com múltiplos arquivos alterados, novas rotinas e ajustes em bots, API e estrutura de tarefas.

## ✨ Tipo de Mudança

- [x] Nova funcionalidade
- [x] Correção de bug
- [x] Refatoração
- [x] Melhoria de performance
- [x] Ajustes estruturais / organização de código
- [x] Infraestrutura / configuração
- [x] Documentação
- [ ] Outro (descrever abaixo)

## 🧩 O que foi alterado

- Diversos arquivos do backend modificados, incluindo:
  - Novos bots e rotinas Celery
  - Ajustes em controllers de tribunais (PJE, ESAJ, Projudi, etc)
  - Refatoração de recursos Selenium e drivers
  - Melhoria na estrutura de autenticação e gerenciamento de credenciais
  - Atualização de configurações e templates
  - Correções em rotas da API e validações de formulários
  - Ajustes em modelos SQLAlchemy
  - Melhoria de performance em tasks assíncronas

## 🏗️ Impacto Técnico

- Mudanças na arquitetura do backend, especialmente em task_manager, controllers e resources
- Novos padrões para bots e tasks
- Possível necessidade de atualização de dependências e arquivos de configuração
- Atenção à compatibilidade com PostgreSQL, Redis, MinIO e Selenium

## ⚠️ Breaking Changes

- [x] Não
- [ ] Sim (descrever abaixo)

## 🧪 Testes e Validação

Mudanças validadas manualmente:

- Importação do backend sem erros
- Execução de bots e tasks Celery
- Testes manuais em endpoints da API
- Linting com ruff check

## 🧹 Manutenção e Qualidade

- [x] Código morto removido
- [x] Imports/arquivos desnecessários removidos
- [x] Melhorias de legibilidade
- [x] Tipagem ou validações aprimoradas
- [x] Comentários ou documentação adicionados

## 📚 Observações para Revisão

- Revisar integração de novas rotinas Celery e bots
- Atenção a mudanças em controllers e recursos Selenium
- Verificar compatibilidade de configurações e dependências
- Sugestão: Validar manualmente principais fluxos após merge

## 🚀 Próximos Passos (Opcional)

- Implementar testes automatizados
- Documentar novas rotinas e endpoints
- Avaliar migração para novas versões de dependências
