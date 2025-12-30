# Documentação do CrawJUD Backend

Este diretório contém a documentação completa de todos os módulos Python do backend CrawJUD.

## Estrutura

A estrutura de diretórios nesta pasta espelha exatamente a estrutura do código fonte em `backend/`, facilitando a navegação.

```
docs/
├── api/                    # API REST Flask
│   ├── _forms/            # Formulários de validação de requisições
│   ├── base/              # Classes base SQLAlchemy e SocketIO
│   ├── decorators/        # Decoradores (CORS, auth, logging)
│   ├── resources/         # Recursos compartilhados da API
│   └── routes/            # Endpoints da API
├── common/                # Componentes comuns
│   └── exceptions/        # Exceções customizadas
├── config/                # Configurações da aplicação
│   └── _log/             # Configuração de logging
├── controllers/           # Controladores dos sistemas judiciais
├── extensions/            # Extensões Flask (MinIO, DB)
├── interfaces/            # Interfaces e schemas de dados
├── models/                # Modelos SQLAlchemy
├── resources/             # Recursos reutilizáveis
│   ├── auth/             # Autenticação nos sistemas judiciais
│   ├── driver/           # Wrappers do Selenium WebDriver
│   ├── elements/         # Seletores de elementos web
│   ├── managers/         # Gerenciadores de recursos
│   └── queues/           # Filas de processamento
├── task_manager/          # Tarefas Celery
│   ├── bots/             # Robôs de automação
│   │   ├── admin/        # Tarefas administrativas
│   │   ├── buscadores/   # Buscadores de processos
│   │   ├── calculadoras/ # Calculadoras de custas
│   │   ├── capa/         # Extratores de capa processual
│   │   ├── emissao/      # Emissão de documentos
│   │   ├── habilitacao/  # Habilitação de advogados
│   │   ├── intimacoes/   # Consulta de intimações
│   │   ├── movimentacao/ # Rastreamento de movimentações
│   │   ├── protocolo/    # Protocolos e peticionamento
│   │   └── provisionamento/ # Provisionamento de processos
│   └── tasks/            # Definições de tarefas Celery
├── types_app/             # Definições de tipos
└── utilities/             # Funções utilitárias

```

## Convenções

Cada arquivo `.py` do backend possui um arquivo `.py.md` correspondente na mesma estrutura de diretórios.

**Exemplo:**
- Arquivo fonte: `backend/api/__init__.py`
- Documentação: `docs/api/__init__.py.md`

## Navegação Rápida

### Principais Pontos de Entrada

- [**__init__.py**](./__init__.py.md) - Ponto de entrada principal da aplicação
- [**__main__.py**](./__main__.py.md) - CLI Typer para executar API/Celery

### API Flask

- [**api/__init__.py**](./api/__init__.py.md) - Factory da aplicação Flask
- [**api/routes/**](./api/routes/) - Rotas e endpoints da API
- [**api/decorators/_api.py**](./api/decorators/_api.py.md) - Decorador CORS

### Modelos de Dados

- [**models/_users.py**](./models/_users.py.md) - Modelo de usuários
- [**models/_bot.py**](./models/_bot.py.md) - Modelo de bots e execuções
- [**models/_jwt.py**](./models/_jwt.py.md) - Modelo de tokens JWT

### Controladores dos Sistemas Judiciais

- [**controllers/pje.py**](./controllers/pje.py.md) - Controlador PJe
- [**controllers/esaj.py**](./controllers/esaj.py.md) - Controlador ESAJ
- [**controllers/projudi.py**](./controllers/projudi.py.md) - Controlador Projudi
- [**controllers/elaw.py**](./controllers/elaw.py.md) - Controlador e-law
- [**controllers/jusds.py**](./controllers/jusds.py.md) - Controlador JusDS

### Robôs de Automação

#### Por Sistema Judicial

##### PJe (Processo Judicial Eletrônico)
- [**task_manager/bots/buscadores/processos/**](./task_manager/bots/buscadores/processos/) - Busca de processos
- [**task_manager/bots/capa/pje/**](./task_manager/bots/capa/pje/) - Extração de capa processual
- [**task_manager/bots/movimentacao/pje/**](./task_manager/bots/movimentacao/pje/) - Movimentações processuais
- [**task_manager/bots/protocolo/pje/**](./task_manager/bots/protocolo/pje/) - Protocolos e peticionamento

##### ESAJ (e-SAJ)
- [**task_manager/bots/buscadores/pagamentos/esaj/**](./task_manager/bots/buscadores/pagamentos/esaj/) - Busca de guias
- [**task_manager/bots/capa/esaj/**](./task_manager/bots/capa/esaj/) - Extração de dados processuais
- [**task_manager/bots/emissao/esaj/**](./task_manager/bots/emissao/esaj/) - Emissão de guias
- [**task_manager/bots/protocolo/esaj/**](./task_manager/bots/protocolo/esaj/) - Protocolos

##### Projudi
- [**task_manager/bots/capa/projudi/**](./task_manager/bots/capa/projudi/) - Extração de capa
- [**task_manager/bots/intimacoes/projudi/**](./task_manager/bots/intimacoes/projudi/) - Consulta de intimações
- [**task_manager/bots/movimentacao/projudi/**](./task_manager/bots/movimentacao/projudi/) - Movimentações

##### e-law
- [**task_manager/bots/admin/elaw/**](./task_manager/bots/admin/elaw/) - Administração e automações
- [**task_manager/bots/provisionamento/elaw.py**](./task_manager/bots/provisionamento/elaw.py.md) - Provisionamento

##### JusDS
- [**task_manager/bots/admin/jusds/**](./task_manager/bots/admin/jusds/) - Administração e automações
- [**task_manager/bots/provisionamento/jusds.py**](./task_manager/bots/provisionamento/jusds.py.md) - Provisionamento

### Recursos Auxiliares

- [**resources/auth/**](./resources/auth/) - Autenticação nos sistemas
- [**resources/driver/**](./resources/driver/) - WebDriver e elementos web
- [**resources/formatadores.py**](./resources/formatadores.py.md) - Funções de formatação
- [**resources/assinador.py**](./resources/assinador.py.md) - Assinatura digital

## Sobre a Documentação

Esta documentação foi gerada automaticamente com base no código fonte Python do projeto. Cada arquivo de documentação inclui:

- **Propósito**: Descrição do módulo
- **Dependências Principais**: Imports mais relevantes
- **Classes**: Estrutura e métodos de cada classe
- **Funções**: Assinaturas e exemplos de uso
- **Constantes**: Constantes definidas no módulo

## Padrões de Documentação

A documentação segue as diretrizes:

- **Idioma**: Português
- **Formato**: Markdown
- **Estilo**: Presente do indicativo, voz ativa
- **Exemplos**: Incluídos quando aplicável
- **Tipagem**: Explícita em todos os parâmetros e retornos

Para mais detalhes sobre os padrões, consulte:
- [Diretrizes Markdown](../.github/instructions/doc-markdown.instructions.md)
- [Padrão Python](../.github/instructions/doc-python.instructions.md)

## Sistemas Judiciais Suportados

O CrawJUD oferece automação para os seguintes sistemas:

| Sistema | Sigla | Descrição |
|---------|-------|-----------|
| Processo Judicial Eletrônico | PJe | Sistema unificado de tramitação judicial |
| e-SAJ | ESAJ | Sistema de Automação da Justiça |
| Projudi | Projudi | Processo Judicial Digital |
| e-law | elaw | Sistema de gestão processual |
| JusDS | JusDS | Sistema de Diligências e Sentenças |
| CSI | CSI | Central de Serviços Integrados |
| Caixa | Caixa | Emissão de guias bancárias |

## Como Usar Esta Documentação

1. **Navegue pela estrutura** de diretórios para encontrar o módulo desejado
2. **Consulte o propósito** de cada arquivo para entender sua função
3. **Explore as classes e funções** documentadas com seus parâmetros e retornos
4. **Use os exemplos de código** como referência para implementação

## Manutenção

Esta documentação é mantida automaticamente. Para atualizá-la:

```bash
python /tmp/generate_docs.py
```

---

**Última atualização**: 2025-12-30
**Total de arquivos documentados**: 217
