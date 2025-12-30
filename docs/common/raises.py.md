# common/raises.py

## Propósito

Forneça funções utilitárias para lançar exceções customizadas.

Este módulo contém funções para lançar erros específicos
relacionados à autenticação, execução e validação.

## Dependências Principais

- `__future__`
- `backend.common.exceptions.validacao`
- `exceptions`
- `typing`

## Função: `raise_password_token()`

Password token error.

Raises:
    PasswordTokenError: PasswordTokenError

**Retorna:** NoReturn

### Exemplo de Uso

```python
resultado = raise_password_token()
```

## Função: `raise_execution_error()`

Lance erro de execução com mensagem personalizada.

Args:
    message (str): Mensagem de erro a ser exibida.
    exc (Exception): Exceção original capturada.

Raises:
    ExecutionError: Erro de execução.

**Parâmetros:**

- `message` (str)
- `exc` (Exception | None)

**Retorna:** NoReturn

### Exemplo de Uso

```python
resultado = raise_execution_error(message, exc)
```

## Função: `auth_error()`

Lance erro de autenticação.

Raises:
    ExecutionError: Erro de autenticação.

**Retorna:** NoReturn

### Exemplo de Uso

```python
resultado = auth_error()
```

## Função: `value_error()`

Lance erro de validação de valor informado.

Raises:
    ValidacaoStringError: Valor não corresponde ao esperado.

**Retorna:** NoReturn

### Exemplo de Uso

```python
resultado = value_error()
```

