# api/routes/web/_bot.py

## Propósito

Log bot.

## Dependências Principais

- `backend.interfaces.payloads`
- `backend.models`
- `backend.types_app`
- `backend.utilities`
- `contextlib`
- `datetime`
- `json`
- `pathlib`
- `tempfile`
- `threading`

## Classe: `CredenciaisSelect`

**Herda de:** `TypedDict`

### Atributos

- `value` (int)
- `text` (str)

## Classe: `Execucao`

**Herda de:** `TypedDict`

### Atributos

- `Id` (0)
- `bot` (str)
- `pid` (str)
- `status` (str)
- `data_inicio` (str)
- `data_fim` (str)

## Função: `is_sistema()`

Verifique se o valor informado pertence aos sistemas cadastrados.

Args:
    valor (Sistemas): Valor a ser verificado.

Returns:
    bool: Indica se o valor está em SISTEMAS.

**Parâmetros:**

- `valor` (Sistemas)

**Retorna:** bool

### Exemplo de Uso

```python
resultado = is_sistema(valor)
```

## Função: `on_listagem_execucoes()`

Lista execuções dos bots do usuário autenticado.

**Parâmetros:**

- `self` (BlueprintNamespace)

**Retorna:** list[Execucao]

### Exemplo de Uso

```python
resultado = on_listagem_execucoes(self)
```

## Função: `on_logbot()`

Log bot.

**Parâmetros:**

- `self` (BlueprintNamespace)
- `data` (Message)

### Exemplo de Uso

```python
on_logbot(self, data)
```

## Função: `on_listagem()`

Lista todos os bots disponíveis para o usuário autenticado.

Returns:
    list[BotInfo]: Lista de bots disponíveis para o usuário.

**Parâmetros:**

- `self` (BlueprintNamespace)

**Retorna:** list[BotInfo]

### Exemplo de Uso

```python
resultado = on_listagem(self)
```

## Função: `on_bot_stop()`

Registre parada do bot e salve log.

**Parâmetros:**

- `self` (BlueprintNamespace)
- `data` (dict[str, str])

### Exemplo de Uso

```python
on_bot_stop(self, data)
```

## Função: `on_join_room()`

Adicione usuário à sala e retorne logs.

**Parâmetros:**

- `self` (BlueprintNamespace)
- `data` (dict[str, str])

**Retorna:** list[str]

### Exemplo de Uso

```python
resultado = on_join_room(self, data)
```

## Função: `on_provide_credentials()`

Lista as credenciais disponíveis para o sistema informado.

**Parâmetros:**

- `self` (BlueprintNamespace)
- `data` (dict[Literal['sistema'], Sistemas])

**Retorna:** list[CredenciaisSelect]

### Exemplo de Uso

```python
resultado = on_provide_credentials(self, data)
```

## Função: `on_connect()`

Log bot.

**Parâmetros:**

- `self` (BlueprintNamespace)

### Exemplo de Uso

```python
on_connect(self)
```

## Função: `on_disconnect()`

Log bot.

**Parâmetros:**

- `self` (BlueprintNamespace)

### Exemplo de Uso

```python
on_disconnect(self)
```

