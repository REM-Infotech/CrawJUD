# resources/formatadores.py

## Propósito

Forneça funções utilitárias para formatar strings.

Este módulo contém funções para remover acentos e caracteres
especiais, tornando textos seguros para nomes de arquivos.

## Dependências Principais

- `__future__`
- `backend.types_app`
- `datetime`
- `pandas`
- `secrets`
- `typing`
- `unicodedata`
- `werkzeug.utils`

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

## Função: `random_base36()`

Gere string aleatória em base 36 para identificadores.

Returns:
    str: Valor aleatório em base 36 como string.

**Retorna:** str

### Exemplo de Uso

```python
resultado = random_base36()
```

## Função: `normalizar()`

Normalize espaços em branco em uma string.

Args:
    txt (str): Texto a ser normalizado.

Returns:
    str: Texto com espaços simples entre palavras.

**Parâmetros:**

- `txt` (str)

**Retorna:** str

### Exemplo de Uso

```python
resultado = normalizar(txt)
```

## Função: `format_data()`

Formata datas ou valores nulos para string legível.

Args:
    value (AnyType): Valor a ser formatado.

Returns:
    str: Data formatada ou string vazia se nulo.

**Parâmetros:**

- `value` (AnyType)

**Retorna:** str

### Exemplo de Uso

```python
resultado = format_data(value)
```

## Função: `format_float()`

Formata número float para string com duas casas decimais.

Args:
    value (AnyType): Número a ser formatado.

Returns:
    str: Número formatado com vírgula como separador decimal.

**Parâmetros:**

- `value` (AnyType)

**Retorna:** str

### Exemplo de Uso

```python
resultado = format_float(value)
```

