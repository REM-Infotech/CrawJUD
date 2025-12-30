# resources/managers/cert_manager.py

## Propósito

Gerencia operações com certificados digitais no Windows.

Inclui funções para instalar e remover certificados PFX via PowerShell.

## Dependências Principais

- `__future__`
- `backend.types_app`
- `subprocess`
- `typing`

## Classe: `CertManagerError`

Lança erro personalizado para operações de certificado.

**Herda de:** `Exception`

### Métodos

#### `__init__()`

**Parâmetros:**

- `self` (Any)
- `mensagem` (str)

## Classe: `CertManager`

Gerencie certificados digitais no Windows via PowerShell.

### Atributos

- `thumbprint` (str)

### Métodos

#### `_run_ps()`

Execute comando PowerShell e retorne saída padrão.

Args:
    script (str): Script PowerShell a ser executado.

Returns:
    str: Saída padrão do comando PowerShell.

Raises:
    CertManagerError: Se o comando retornar erro.

**Parâmetros:**

- `cls` (Any)
- `script` (str)

**Retorna:** str

#### `install_pfx()`

Instale certificado PFX no repositório CurrentUser\My.

Args:
    pfx_path (str): Caminho do arquivo PFX.
    pfx_password (str): Senha do certificado.

Returns:
    str: Thumbprint do certificado instalado.

**Parâmetros:**

- `cls` (Any)
- `pfx_path` (str)
- `pfx_password` (str)

**Retorna:** str

#### `uninstall_pfx()`

Remova certificado pelo thumbprint e retorne status booleano.

Returns:
    bool: True se removido, False se não encontrado.

**Parâmetros:**

- `cls` (Any)

**Retorna:** bool

