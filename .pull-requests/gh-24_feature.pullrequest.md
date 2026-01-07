## ---

## [GH-24] Feature - Migração arquitetural completa para branch devel

---

## 📖 Descrição

Este Pull Request realiza a migração e integração completa da branch devel na main, promovendo uma evolução arquitetural significativa no backend CrawJUD.

Inclui:

- Objetivo principal: Atualizar o sistema para uma arquitetura moderna baseada em async/await, com novas funcionalidades e melhor organização de módulos.
- Motivação: Atender demandas de escalabilidade, performance, automação avançada e integração com novas tecnologias (MinIO, Celery, Socket.IO, OCR, etc).
- Impacto esperado: Expansão de capacidades (+60% funcionalidades), melhor separação de responsabilidades, suporte a microserviços e maior flexibilidade para desenvolvimento futuro.

## ---

## [GH-24] Refatoração e Modernização - Bot Jusds Provisionamento

---

## 📖 Descrição

Este Pull Request realiza uma refatoração profunda e modernização do bot de provisionamento do sistema Jusds.

- Objetivo principal: Simplificar e tornar mais robusta a automação de provisionamento Jusds.
- Motivação: Melhorar legibilidade, segurança, tipagem e facilitar manutenção futura.
- Impacto esperado: Código mais limpo, abstrações claras, menos bugs e maior facilidade para evoluções.

## ✨ Tipo de Mudança

- [ ] Nova funcionalidade
- [x] Correção de bug
- [x] Refatoração
- [x] Melhoria de performance
- [x] Ajustes estruturais / organização de código
- [ ] Infraestrutura / configuração
- [ ] Documentação
- [ ] Outro (descrever abaixo)

## 🧩 O que foi alterado

- Remoção de classes antigas de tabela/iteradores
- Criação de abstrações para campos e elementos do provisionamento
- Tipagem aprimorada (Literal, TypedDict)
- Melhoria na lógica de preenchimento de campos e envio de dados Selenium
- Ajustes em XPATHs, CSS Selectors e estrutura dos elementos
- Remoção de docstrings redundantes e código morto
- Adição de novos campos e lógica para manipulação de riscos, objetos e status de eventos

## 🏗️ Impacto Técnico

- Modernização do fluxo de automação do bot Jusds Provisionamento
- Código mais legível, seguro e fácil de manter
- Facilita futuras expansões e integrações
- Possíveis efeitos colaterais em scripts que dependiam da estrutura antiga

## ⚠️ Breaking Changes

- [x] Não
- [ ] Sim (descrever abaixo)

## 🧪 Testes e Validação

- Testes manuais nos fluxos de automação Jusds Provisionamento
- Validação dos campos, status e manipulação de riscos

## 🧹 Manutenção e Qualidade

- [x] Código morto removido
- [x] Imports/arquivos desnecessários removidos
- [x] Melhorias de legibilidade
- [x] Tipagem ou validações aprimoradas
- [x] Comentários ou documentação adicionados

## 📚 Observações para Revisão

- Atenção especial à compatibilidade do bot Jusds Provisionamento
- Scripts que dependiam da estrutura antiga podem precisar de ajustes
- Decisão técnica: priorizar legibilidade, abstração e tipagem

## 🚀 Próximos Passos (Opcional)

- Automatizar testes do bot Jusds Provisionamento
- Melhorar cobertura de cenários de risco e objeto
