## ---

## [GH-25] Refactor - Estrutura e utilitários do projeto

---

## 📖 Descrição

Este Pull Request realiza uma grande refatoração estrutural no backend do CrawJUD, reorganizando módulos, removendo arquivos obsoletos e consolidando funções utilitárias. Foram criados novos utilitários para geração de IDs, conversão de strings e aprimorado o gerenciamento de tarefas de e-mail. O objetivo principal é melhorar a organização, legibilidade e extensibilidade do sistema, facilitando a manutenção e evolução futura.

- O principal objetivo é modernizar e modularizar a base de código, reduzindo redundâncias e facilitando a adição de novas funcionalidades.
- A necessidade surgiu devido à complexidade crescente e à presença de padrões antigos que dificultavam a manutenção.
- O impacto esperado é um sistema mais limpo, com menor acoplamento entre módulos e maior facilidade para onboarding de novos desenvolvedores.

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

- Reorganização completa dos diretórios de bots, tasks e extensões
- Remoção de módulos e arquivos duplicados ou obsoletos
- Criação de utilitários para geração de IDs, conversão de formatos e validação de strings
- Refatoração do sistema de tasks Celery, centralizando o registro e a definição de tasks
- Melhoria no gerenciamento de templates e envio de e-mails
- Ajustes em imports, tipagem e padronização de métodos

## 🏗️ Impacto Técnico

- Mudanças relevantes na arquitetura dos módulos de tasks, bots e extensões
- Substituição de funções e classes antigas por novas abstrações
- Possível necessidade de ajuste em scripts de deploy e inicialização
- Dependências internas reorganizadas, podendo impactar integrações customizadas
- Não há breaking changes para APIs públicas, mas integrações internas podem exigir revisão

## ⚠️ Breaking Changes

- [x] Não
- [ ] Sim (descrever abaixo)

## 🧪 Testes e Validação

- Testes manuais de importação dos principais módulos
- Execução dos comandos de inicialização do backend e Celery
- Validação dos endpoints principais da API
- Verificação do envio de e-mails de notificação

## 🧹 Manutenção e Qualidade

- [x] Código morto removido
- [x] Imports/arquivos desnecessários removidos
- [x] Melhorias de legibilidade
- [x] Tipagem ou validações aprimoradas
- [x] Comentários ou documentação adicionados

## 📚 Observações para Revisão

- Refatoração extensa, recomenda-se revisão atenta dos pontos de integração entre módulos
- Decisões técnicas documentadas nos docstrings e comentários dos principais arquivos
- Não há alterações em endpoints externos, mas a estrutura interna foi profundamente modificada
- Limitações: não há cobertura automatizada de testes, validação foi manual

## 🚀 Próximos Passos (Opcional)

- Implementar testes automatizados para os novos utilitários e tasks
- Documentar padrões de desenvolvimento para novos módulos
- Avaliar migração futura para framework async (Quart)
