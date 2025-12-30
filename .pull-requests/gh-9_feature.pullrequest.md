## [GH-9] feature - Gerenciamento de credenciais e novas rotas API

## 📖 Descrição

Este Pull Request implementa o gerenciamento de credenciais para robôs, incluindo rotas para cadastro e deleção de credenciais. Também adiciona novas rotas para autenticação e gerenciamento de bots, além de refatorar a estrutura de namespaces para API e WebSocket.

O objetivo principal é centralizar e padronizar o gerenciamento de credenciais e bots, facilitando a manutenção e evolução do sistema. A necessidade surgiu da demanda por maior flexibilidade e segurança no controle de credenciais, além de uma arquitetura mais limpa para rotas e handlers.

O impacto esperado é a melhoria na organização do backend, maior clareza nos fluxos de autenticação e manipulação de bots, e redução de código legado.

## ✨ Tipo de Mudança

- [x] Nova funcionalidade
- [ ] Correção de bug
- [x] Refatoração
- [ ] Melhoria de performance
- [x] Ajustes estruturais / organização de código
- [ ] Infraestrutura / configuração
- [ ] Documentação
- [ ] Outro (descrever abaixo)

## 🧩 O que foi alterado

- Criação de rotas para cadastro e deleção de credenciais de robôs, com abstração de lógica em classe dedicada.
- Novas rotas para autenticação e gerenciamento de bots, separando responsabilidades e facilitando manutenção.
- Refatoração dos namespaces de API e WebSocket, utilizando BlueprintNamespace para padronizar eventos e handlers.
- Ajustes em funções de conexão e manipulação de eventos, removendo duplicidade e melhorando clareza.
- Remoção de arquivos e imports obsoletos, reduzindo código morto e melhorando legibilidade.
- Correção de importações e organização de módulos para refletir a nova estrutura.

## 🏗️ Impacto Técnico

- Mudanças na arquitetura de rotas e namespaces
- Refatoração de handlers para uso de BlueprintNamespace
- Possível impacto em integrações que dependam das rotas antigas
- Melhoria na organização e manutenção do código

## ⚠️ Breaking Changes

- [x] Não
- [ ] Sim (descrever abaixo)

## 🧪 Testes e Validação

As mudanças foram validadas manualmente em ambiente de desenvolvimento. Não houve alteração em arquivos de teste automatizado.

## 🧹 Manutenção e Qualidade

- [x] Código morto removido
- [x] Imports/arquivos desnecessários removidos
- [x] Melhorias de legibilidade
- [x] Tipagem ou validações aprimoradas
- [x] Comentários ou documentação adicionados

## 📚 Observações para Revisão

- Refatoração significativa na estrutura de rotas e namespaces
- Atenção a possíveis integrações externas que dependam das rotas removidas ou alteradas
- Decisões técnicas para padronização de eventos e handlers

## 🚀 Próximos Passos (Opcional)

- Adicionar testes automatizados para as novas rotas e handlers
- Documentar exemplos de uso das novas rotas de credenciais e bots
