# api/routes/web/_admin.py

## Propósito

Módulo do sistema CrawJUD.

## Dependências Principais

- `__future__`
- `backend.api.base`
- `backend.api.routes._blueprints`
- `backend.models`
- `datetime`
- `flask_jwt_extended`
- `typing`
- `zoneinfo`

## Classe: `CredencialItem`

**Herda de:** `TypedDict`

### Atributos

- `Id` (int)
- `nome_credencial` (str)
- `tipo_autenticacao` (str)

## Classe: `UsuarioItem`

**Herda de:** `TypedDict`

### Atributos

- `Id` (int)
- `nome_Usuario` (str)
- `login_usuario` (str)
- `email` (str)
- `ultimo_login` (str)

## Função: `disconnect()`

**Parâmetros:**

- `self` (BlueprintNamespace)
- `args` (Any)

### Exemplo de Uso

```python
disconnect(self, args)
```

## Função: `connect()`

**Parâmetros:**

- `self` (BlueprintNamespace)

### Exemplo de Uso

```python
connect(self)
```

## Função: `listagem_credenciais()`

**Parâmetros:**

- `self` (BlueprintNamespace)

**Retorna:** list[CredencialItem]

### Exemplo de Uso

```python
resultado = listagem_credenciais(self)
```

## Função: `listagem_usuarios()`

**Parâmetros:**

- `self` (BlueprintNamespace)

**Retorna:** list[UsuarioItem]

### Exemplo de Uso

```python
resultado = listagem_usuarios(self)
```

