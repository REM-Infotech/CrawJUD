# interfaces/elaw/main.py

## Propósito

Gerencie e manipule dados do eLaw com utilitários.

Este módulo fornece a classe ElawData para manipulação de dados
relacionados ao sistema eLaw, incluindo métodos para limpeza,
atualização e formatação de informações.

## Dependências Principais

- `__future__`
- `backend.task_manager.constants.data._bots.cidades`
- `backend.types_app`
- `collections`
- `typing`

## Classe: `ElawData`

Gerencie e manipule dados do eLaw com métodos utilitários.

**Herda de:** `UserDict`

### Métodos

#### `__init__()`

Inicialize a instância ElawData com dados fornecidos.

Args:
    values (Dict | None): Dados iniciais do eLaw.
    **kwargs (AnyType): Argumentos adicionais.

**Parâmetros:**

- `self` (Any)
- `values` (Dict | None)

#### `_remove_empty_keys()`

Remove chaves com valores vazios ou None.

**Parâmetros:**

- `self` (Any)

#### `_update_tipo_parte_contraria()`

Atualize 'TIPO_PARTE_CONTRARIA' se 'TIPO_EMPRESA' for 'RÉU'.

**Parâmetros:**

- `self` (Any)

#### `_update_capital_interior()`

Atualize o campo 'CAPITAL_INTERIOR' conforme 'COMARCA'.

**Parâmetros:**

- `self` (Any)

**Retorna:** Dict[str, str]

#### `_set_data_inicio()`

Defina 'DATA_INICIO' se ausente e 'DATA_LIMITE' presente.

**Parâmetros:**

- `self` (Any)

**Retorna:** Dict[str, str]

#### `_format_numeric_values()`

Formata valores numéricos para duas casas decimais.

**Parâmetros:**

- `self` (Any)

