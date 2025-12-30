# resources/__init__.py

## Propósito

Pacote público para recursos do sistema.

Contém arquivos e utilitários de recursos compartilhados.

## Dependências Principais

- `auth.pje`
- `backend.task_manager.constants`
- `formatadores`
- `iterators.pje`
- `re`

## Função: `camel_to_snake()`

Converta string CamelCase para snake_case.

Args:
    name (str): String no formato CamelCase.

Returns:
    str: String convertida para snake_case.

**Parâmetros:**

- `name` (str)

**Retorna:** str

### Exemplo de Uso

```python
resultado = camel_to_snake(name)
```

## Função: `value_check()`

Verifique se valor não está em constantes proibidas.

Args:
    label (str): Rótulo do campo.
    valor (str): Valor a ser verificado.

Returns:
    bool: True se valor for permitido, senão False.

**Parâmetros:**

- `label` (str)
- `valor` (str)

**Retorna:** bool

### Exemplo de Uso

```python
resultado = value_check(label, valor)
```

