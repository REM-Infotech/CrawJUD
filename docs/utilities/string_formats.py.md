# utilities/string_formats.py

## Propósito

Pacote de útilitários de formatação de strings para o CrawJUD.

## Dependências Principais

- `IP2Location`
- `contextlib`
- `datetime`
- `flask`
- `pathlib`
- `re`
- `zoneinfo`

## Constantes

- `WORKDIR_PATH`
- `T_PATERN`
- `T_PATERN2`
- `TIME_PATTERNS`

## Função: `format_time()`

Formata data/hora para string legível ou retorne valor original.

**Parâmetros:**

- `val` (datetime | None)

**Retorna:** str | None

### Exemplo de Uso

```python
resultado = format_time(val)
```

## Função: `get_ip2location_instance()`

Obtenha uma instância do banco de dados IP2Location.

Returns:
    IP2Location: Instância carregada do banco de dados IP2Location.

**Retorna:** IP2Location

### Exemplo de Uso

```python
resultado = get_ip2location_instance()
```

## Função: `detect_datetime_format()`

Detecta o formato da string de data/hora e retorne um objeto datetime.

Args:
    str_dt (str): String de data/hora a ser analisada.

Returns:
    datetime: Objeto datetime correspondente à string fornecida.

Raises:
    ValueError: Quando o formato da string não é reconhecido.

**Parâmetros:**

- `str_dt` (str)

**Retorna:** datetime

### Exemplo de Uso

```python
resultado = detect_datetime_format(str_dt)
```

## Função: `load_timezone()`

Obtenha o fuso horário do cliente com base no endereço IP.

Returns:
    str: Nome do fuso horário no formato 'America/Cidade'.

**Retorna:** str

### Exemplo de Uso

```python
resultado = load_timezone()
```

## Função: `update_timezone()`

Atualize o horário informado para o fuso horário do cliente.

Args:
    dt (datetime | str): Data/hora a ser ajustada para o fuso do cliente.

Returns:
    str: Horário ajustado para o fuso do cliente no formato HH:MM:SS.

**Parâmetros:**

- `dt` (datetime | str)

**Retorna:** datetime

### Exemplo de Uso

```python
resultado = update_timezone(dt)
```

