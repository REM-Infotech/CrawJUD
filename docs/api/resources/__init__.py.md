# api/resources/__init__.py

## Propósito

Recursos da API.

## Dependências Principais

- `re`
- `secrets`
- `string`
- `typing`
- `unicodedata`
- `werkzeug.utils`

## Função: `gerar_id()`

Gere identificador aleatório de 8 caracteres alfanuméricos.

Returns:
    LiteralString: ID com letras e números aleatórios.

**Retorna:** LiteralString

### Exemplo de Uso

```python
resultado = gerar_id()
```

## Função: `camel_to_snake()`

Convenção de uma string CamelCase para snake_case.

Returns:
    str: String convertida para snake_case.

**Parâmetros:**

- `name` (str)

**Retorna:** str

### Exemplo de Uso

```python
resultado = camel_to_snake(name)
```

## Função: `formata_string()`

Remova acentos e caracteres especiais da string.

Args:
    string (str): Texto a ser formatado.

Returns:
    str: Texto formatado em caixa alta e seguro para nomes
        de arquivo.

**Parâmetros:**

- `string` (str)

**Retorna:** str

### Exemplo de Uso

```python
resultado = formata_string(string)
```

