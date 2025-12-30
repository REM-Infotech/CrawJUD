# resources/keystore.py

## Propósito

Keepass wrapper.

## Dependências Principais

- `__future__`
- `dotenv`
- `pathlib`
- `pykeepass`
- `pykeepass.group`
- `typing`
- `uuid`

## Classe: `KeePassFindEntryKwargs`

Defina os argumentos aceitos para busca de entradas no KeePass.

Args:
    path (list[str]): Caminho dos grupos.
    title (str): Título da entrada.
    username (str): Nome de usuário.
    password (str): Senha.
    url (str): URL associada.
    notes (str): Notas da entrada.
    otp (str): Código OTP.
    string (dict[str, str]): Campos personalizados.
    uuid (pyuuid.UUID): UUID da entrada.
    tags (list[str]): Lista de tags.
    autotype_enabled (bool): Autotype habilitado.
    autotype_sequence (str): Sequência de autotype.
    autotype_window (str): Janela de autotype.
    group (Group): Grupo da entrada.
    first (bool): Retorne apenas o primeiro resultado.
    history (bool): Inclua histórico.
    recursive (bool): Busca recursiva.
    regex (bool): Use regex na busca.
    flags (str): Flags adicionais.

**Herda de:** `TypedDict`

### Atributos

- `path` (list[str])
- `title` (str)
- `username` (str)
- `password` (str)
- `url` (str)
- `notes` (str)
- `otp` (str)
- `string` (dict[str, str])
- `uuid` (pyuuid.UUID)
- `tags` (list[str])
- `autotype_enabled` (bool)
- `autotype_sequence` (str)
- `autotype_window` (str)
- `group` (Group)
- `first` (bool)
- `history` (bool)
- `recursive` (bool)
- `regex` (bool)
- `flags` (str)

## Classe: `KeyStore`

Implemente um wrapper para interagir com um banco KeePass via PyKeePass.

Esta classe permite inicializar e buscar entradas em um banco KeePass.

**Herda de:** `PyKeePass`

### Métodos

#### `__init__()`

Inicialize o KeyStore com o arquivo e senha do banco KeePass.

Args:
    arquivo_kdbx (str | None): Caminho do arquivo KeePass.
    senha_kdbx (str | None): Senha do arquivo KeePass.

**Parâmetros:**

- `self` (Any)
- `arquivo_kdbx` (str)
- `senha_kdbx` (str)

#### `find_entries()`

Busque entradas no banco KeePass conforme os critérios informados.

Args:
    kwargs (KeePassFindEntryKwargs): Critérios de busca.
    recursive (bool): Busca recursiva nos grupos.
    path (str | None): Caminho do grupo.
    group (Group | None): Grupo KeePass.

Returns:
    (Entry | list[Entry] | None): Entradas encontradas ou None.

**Parâmetros:**

- `self` (Any)
- `kwargs` (KeePassFindEntryKwargs)

**Retorna:** Entry | list[Entry] | None

