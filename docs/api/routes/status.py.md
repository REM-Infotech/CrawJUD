# api/routes/status.py

## Propósito

Rotas de status da API.

## Dependências Principais

- `__future__`
- `backend.api`
- `backend.extensions`
- `backend.types_app`
- `flask`
- `flask_jwt_extended`
- `typing`

## Função: `health_check()`

**Retorna:** HealtCheck

### Exemplo de Uso

```python
resultado = health_check()
```

## Função: `index()`

**Retorna:** Response

### Exemplo de Uso

```python
resultado = index()
```

## Função: `static_from_root()`

**Retorna:** Response

### Exemplo de Uso

```python
resultado = static_from_root()
```

## Função: `sessao_valida()`

Verifica se a sessão JWT é válida.

Retorna um status 200 se a sessão for válida, caso contrário,
retorna um erro 401.

Returns:
    Response: Resposta HTTP indicando o status da sessão.

**Retorna:** Response

### Exemplo de Uso

```python
resultado = sessao_valida()
```

