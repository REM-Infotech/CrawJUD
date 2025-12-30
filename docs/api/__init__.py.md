# api/__init__.py

## Propósito

Inicialize a aplicação Flask principal da API CrawJUD.

Este módulo configura a aplicação, carrega variáveis de ambiente,
define o contexto de criptografia e fornece a função de criação da app.

## Dependências Principais

- `backend.config`
- `dotenv`
- `dynaconf`
- `flask`
- `passlib.context`
- `werkzeug.middleware.proxy_fix`

## Função: `create_app()`

Crie e configure a aplicação Flask.

Returns:
    Flask: Instância configurada da aplicação Flask.

**Retorna:** Flask

### Exemplo de Uso

```python
resultado = create_app()
```

