## [GH-20] Refatoração - Estrutura, tipagem e documentação

---

## 📖 Descrição

Este Pull Request realiza uma ampla refatoração estrutural e de organização do backend CrawJUD.

Inclui:

- Reorganização de imports e módulos para melhor modularidade
- Melhoria e padronização de tipagens (uso de `typings`)
- Remoção de arquivos e imports não utilizados
- Criação de novos módulos para gerenciamento de dados
- Melhoria de logging e tratamento de erros
- Atualização de dependências no lockfile
- Geração e inclusão de documentação automática em Markdown para os principais módulos

O objetivo é facilitar a manutenção, aumentar a clareza e preparar o projeto para futuras expansões.

## ✨ Tipo de Mudança

- [ ] Nova funcionalidade
- [ ] Correção de bug
- [x] Refatoração
- [x] Melhoria de performance
- [x] Ajustes estruturais / organização de código
- [x] Infraestrutura / configuração
- [x] Documentação
- [ ] Outro (descrever abaixo)

## 🧩 O que foi alterado

- Refatoração de imports e tipagens em todo o backend
- Remoção de duplicidades e código morto
- Criação de novos módulos para abstrações de dados e tasks
- Melhoria de logging, tratamento de exceções e padronização de respostas
- Atualização de dependências no pyproject/uv.lock
- Geração de documentação Markdown para cada módulo principal

## 🏗️ Impacto Técnico

- Mudanças na arquitetura de pacotes e estrutura de diretórios
- Tipagem centralizada em typings/
- Possível necessidade de ajuste em scripts de automação e deploy
- Dependências atualizadas: celery, flask-keepass, flask-socketio, numpy, pillow, typer, etc.
- Documentação agora disponível em docs/backend/

## ⚠️ Breaking Changes

- [x] Sim (descrever abaixo)
- [ ] Não

- Estrutura de imports e paths alterada (ex: `backend.api.base` → `backend.base`)
- Tipos e helpers movidos para typings/
- Scripts externos e integrações podem precisar de ajuste nos imports

## 🧪 Testes e Validação

- Testes manuais de execução dos bots e endpoints
- Validação de importação do backend
- Linting e formatação com ruff
- Verificação de geração e leitura dos arquivos de documentação

## 🧹 Manutenção e Qualidade

- [x] Código morto removido
- [x] Imports/arquivos desnecessários removidos
- [x] Melhorias de legibilidade
- [x] Tipagem ou validações aprimoradas
- [x] Comentários ou documentação adicionados

## 📚 Observações para Revisão

- Atenção especial à compatibilidade de imports em scripts externos
- Verificar se todos os bots e endpoints continuam funcionando após a refatoração
- Documentação gerada cobre apenas módulos principais; detalhamento extra pode ser feito sob demanda

## 🚀 Próximos Passos (Opcional)

- Expandir documentação para todos os módulos auxiliares
- Automatizar geração de documentação em CI
- Revisar e padronizar exemplos de uso em todos os arquivos
