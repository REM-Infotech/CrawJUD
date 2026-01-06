##

---

## [GH-21] Refact - Remoção de componentes obsoletos e melhoria estrutural

---

## 📖 Descrição

Este Pull Request realiza uma ampla refatoração no código base do CrawJUD, removendo módulos obsoletos (KeyStore, Jusds), eliminando arquivos e dependências desnecessárias, e aprimorando a legibilidade e organização dos componentes. Também renomeia a classe FlaskTask para CeleryTask e reestrutura dicionários para melhor padronização. Um delay foi introduzido no processamento de logs para evitar sobrecarga.

- Objetivo principal: Simplificar e modernizar a base de código, reduzindo complexidade e facilitando manutenção.
- Problema: Existência de componentes não utilizados, duplicidade de abstrações e estrutura confusa.
- Impacto: Código mais limpo, fácil de entender e manter, menor risco de bugs relacionados a componentes obsoletos.

## ✨ Tipo de Mudança

- [ ] Nova funcionalidade
- [ ] Correção de bug
- [x] Refatoração
- [x] Melhoria de performance
- [x] Ajustes estruturais / organização de código
- [ ] Infraestrutura / configuração
- [ ] Documentação
- [ ] Outro (descrever abaixo)

## 🧩 O que foi alterado

- Remoção dos módulos KeyStore e Jusds (bots, interfaces, managers)
- Renomeação de FlaskTask para CeleryTask em todo o projeto
- Reestruturação dos dicionários e interfaces para centralização em backend/dicionarios
- Eliminação de constantes duplicadas e padronização de imports
- Introdução de delay no processamento de logs para evitar overload
- Ajustes em bots, controllers e recursos para refletir nova estrutura

## 🏗️ Impacto Técnico

- Mudanças na arquitetura: simplificação da estrutura de tasks e dicionários
- Remoção de dependências (pykeepass, dotenv, etc.)
- Alteração de fluxos de autenticação e manipulação de dados
- Possíveis efeitos colaterais: scripts que dependiam dos módulos removidos deixarão de funcionar

## ⚠️ Breaking Changes

- [x] Não
- [ ] Sim (descrever abaixo)

## 🧪 Testes e Validação

- Testes manuais realizados nos principais bots e endpoints
- Validação de importação do módulo backend
- Linting com ruff para garantir qualidade
- Não há testes automatizados

## 🧹 Manutenção e Qualidade

- [x] Código morto removido
- [x] Imports/arquivos desnecessários removidos
- [x] Melhorias de legibilidade
- [x] Tipagem ou validações aprimoradas
- [x] Comentários ou documentação adicionados

## 📚 Observações para Revisão

- Refatoração extensa, recomenda-se revisão detalhada dos fluxos afetados
- Decisões técnicas: centralização de dicionários, padronização de tasks
- Limitações: ausência de testes automatizados, dependência de validação manual

## 🚀 Próximos Passos (Opcional)

- Avaliar criação de testes automatizados para bots principais
- Monitorar possíveis efeitos colaterais em produção
- Documentar novos padrões e abstrações
