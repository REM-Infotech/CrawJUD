## ---

## [GH-29] Refactor - Migração para Quart e refatoração da base

---

## 📖 Descrição

Este Pull Request migra toda a base do projeto de Flask para Quart, habilitando suporte assíncrono nativo e modernizando a arquitetura. Foram refatorados módulos principais, rotas, blueprints, decorators, tasks Celery, WebSocket e integração JWT, além de ajustes em nomenclaturas e padronização de argumentos (ex: `pid` para `id_execucao`).

Inclui:

- Substituição de Flask/Flask-SocketIO por Quart/Quart-SocketIO
- Refatoração de rotas, blueprints e decorators para async/await
- Ajustes em tasks Celery para contexto Quart
- Atualização de dependências e requirements
- Remoção de código morto e imports obsoletos
- Adaptação de WebSocket para novas namespaces e eventos

O objetivo é preparar o backend para maior escalabilidade, melhor performance e facilitar integrações futuras com recursos assíncronos.

## ✨ Tipo de Mudança

- [ ] Nova funcionalidade
- [ ] Correção de bug
- [x] Refatoração
- [x] Melhoria de performance
- [x] Ajustes estruturais / organização de código
- [x] Infraestrutura / configuração
- [ ] Documentação
- [ ] Outro (descrever abaixo)

## 🧩 O que foi alterado

- Migração completa de Flask para Quart (inclusive dependências e imports)
- Refatoração de rotas, blueprints, decorators e tasks para async/await
- Ajuste de nomenclaturas e argumentos para padronização (ex: `pid` → `id_execucao`)
- Atualização de WebSocket: namespaces, eventos e handlers
- Remoção de código morto e arquivos obsoletos
- Melhoria de logging, organização de arquivos e modularização

## 🏗️ Impacto Técnico

- Mudança estrutural: toda a stack HTTP e WebSocket agora é assíncrona
- Dependências alteradas: quart, quart-socketio, quart-flask-patch, quart-cors, etc
- Possível necessidade de ajustes em integrações externas e scripts de automação
- Fluxos de autenticação, tasks Celery e uploads agora usam contexto Quart
- Possíveis efeitos colaterais em bots e integrações legadas

## ⚠️ Breaking Changes

- [x] Não
- [ ] Sim (descrever abaixo)

## 🧪 Testes e Validação

- Testes manuais de rotas HTTP, autenticação, execução de bots e uploads
- Validação de tasks Celery e WebSocket em ambiente de desenvolvimento
- Verificação de logs e respostas assíncronas

## 🧹 Manutenção e Qualidade

- [x] Código morto removido
- [x] Imports/arquivos desnecessários removidos
- [x] Melhorias de legibilidade
- [x] Tipagem ou validações aprimoradas
- [x] Comentários ou documentação adicionados

## 📚 Observações para Revisão

- Atenção especial à compatibilidade de bots e tasks Celery
- Verificar integrações externas que dependiam de Flask
- Ajustar scripts de automação e deploy para Quart
- Decisão técnica: priorizar async/await e contexto Quart em toda a base

## 🚀 Próximos Passos (Opcional)

- Automatizar testes para rotas e WebSocket
- Revisar documentação para refletir a nova stack
- Avaliar ganhos de performance em produção
