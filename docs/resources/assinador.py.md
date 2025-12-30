# resources/assinador.py

## Propósito

Autenticador PJe.

## Dependências Principais

- `backend.controllers.pje`
- `base64`
- `clear`
- `cryptography.hazmat.primitives.asymmetric.dh`
- `cryptography.hazmat.primitives.asymmetric.dsa`
- `cryptography.hazmat.primitives.asymmetric.ec`
- `cryptography.hazmat.primitives.asymmetric.ed25519`
- `cryptography.hazmat.primitives.serialization`
- `pathlib`
- `tqdm`

## Classe: `ConteudoAssinado`

Classe que representa um conteúdo assinado e sua cadeia de certificados.

Attributes
----------
_chain : list[PKCS12Certificate]
    Cadeia de certificados utilizada na assinatura.
_conteudo_assinado : bytes
    Conteúdo assinado em formato binário.

### Atributos

- `_chain` (list[PKCS12Certificate])
- `_conteudo_assinado` (bytes)

### Métodos

#### `__init__()`

Inicializa o ConteudoAssinado.

Parameters
----------
conteudo_assinado : bytes
    Conteúdo assinado em formato binário.
certificado : PKCS12Certificate
    Certificado utilizado na assinatura.
cadeia : list[PKCS12Certificate]
    Cadeia de certificados utilizada na assinatura.

**Parâmetros:**

- `self` (Any)
- `conteudo_assinado` (bytes)
- `certificado` (PKCS12Certificate)
- `cadeia` (list[PKCS12Certificate])

#### `conteudo_assinado_base64()`

**Parâmetros:**

- `self` (Any)

**Retorna:** str

#### `cadeia_base64()`

**Parâmetros:**

- `self` (Any)

**Retorna:** str

## Classe: `Assinador`

Classe responsável por assinar conteúdos utilizando certificados digitais.

### Atributos

- `_chain` (list[Certificate])
- `bot` (PJeBot)
- `_certificado_carregado` (PKCS12KeyAndCertificates)
- `algoritmos_suportados` (ClassVar[dict[Algoritmos, hashes.HashAlgorithm]])

### Métodos

#### `__init__()`

Inicialize o objeto Assinador com o certificado digital e senha.

Args:
    certificado (str | None): Caminho para o certificado digital.
    senha_certificado (str | None): Senha do certificado digital.

**Parâmetros:**

- `self` (Any)
- `certificado` (str | None)
- `senha_certificado` (str | None)

#### `assinar_conteudo()`

**Parâmetros:**

- `self` (Any)
- `conteudo` (str | bytes)
- `algoritmo_assinatura` (Algoritmos)

**Retorna:** ConteudoAssinado

#### `certificado_carregado()`

**Parâmetros:**

- `self` (Any)

**Retorna:** PKCS12KeyAndCertificates

#### `certificado_carregado()`

**Parâmetros:**

- `self` (Any)
- `valor` (PKCS12KeyAndCertificates)

#### `chave()`

**Parâmetros:**

- `self` (Any)

**Retorna:** PrivateKey

#### `certficado()`

**Parâmetros:**

- `self` (Any)

**Retorna:** PKCS12Certificate | None

#### `cadeia()`

**Parâmetros:**

- `self` (Any)

**Retorna:** list[PKCS12Certificate]

