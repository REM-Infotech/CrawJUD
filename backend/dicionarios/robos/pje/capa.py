from __future__ import annotations

from typing import Literal, TypedDict


class PJeCapa(TypedDict):
    NUMERO_PROCESSO: str
    GRAU: str
    REGIAO: str
    TRAZER_ASSUNTOS: Literal["sim", "não"]
    TRAZER_PARTES: Literal["sim", "não"]
    TRAZER_AUDIENCIAS: Literal["sim", "não"]
    TRAZER_MOVIMENTACOES: Literal["sim", "não"]


class AssuntoPJe(TypedDict):
    """Defina os campos dos assuntos do processo judicial no padrão PJe.

    Args:
        ID_PJE (int): Identificador único do processo no PJE.
        PROCESSO (str): Número do processo judicial.
        ASSUNTO_COMPLETO (str): Descrição completa do assunto.
        ASSUNTO_RESUMIDO (str): Descrição resumida do assunto.

    Returns:
        AssuntoPJe: Dicionário tipado com os dados dos assuntos.

    """

    ID_PJE: int
    PROCESSO: str
    ASSUNTO_COMPLETO: str
    ASSUNTO_RESUMIDO: str


class AudienciaProcessoPJe(TypedDict):
    """Defina os campos das audiências do processo no padrão PJe.

    Args:
        ID_PJE (int): Identificador único do processo no PJE.
        NUMERO_PROCESSO (str): Número do processo judicial.
        TIPO_AUDIENCIA (str): Tipo da audiência.
        MODO_AUDIENCIA (str): Modo de realização da audiência.
        STATUS (str): Status da audiência.
        DATA_INICIO (str): Data de início da audiência.
        DATA_FIM (str): Data de término da audiência.
        DATA_MARCACAO (str): Data de marcação da audiência.

    """

    ID_PJE: int
    NUMERO_PROCESSO: str
    TIPO_AUDIENCIA: str
    MODO_AUDIENCIA: str
    STATUS: str
    DATA_INICIO: str
    DATA_FIM: str
    DATA_MARCACAO: str


class PartePJe(TypedDict):
    """Defina os campos das partes do processo judicial no padrão PJe.

    Args:
        ID_PJE (int): Identificador único do processo no PJE.
        NOME (str): Nome da parte.
        DOCUMENTO (str): Documento da parte.
        TIPO_DOCUMENTO (str): Tipo do documento.
        TIPO_PARTE (str): Tipo da parte (autor/réu).
        TIPO_PESSOA (str): Tipo da pessoa (física/jurídica).
        PROCESSO (str): Número do processo.
        POLO (str): Polo da parte (ativo/passivo).
        PARTE_PRINCIPAL (bool): Indica se é parte principal.

    """

    ID_PJE: int
    NOME: str
    DOCUMENTO: str
    TIPO_DOCUMENTO: str
    TIPO_PARTE: str
    TIPO_PESSOA: str
    PROCESSO: str
    POLO: str
    PARTE_PRINCIPAL: bool


class RepresentantePJe(TypedDict):
    """Defina os campos dos representantes das partes no padrão PJe.

    Args:
        ID_PJE (int): Identificador único do processo no PJE.
        NOME (str): Nome do representante.
        DOCUMENTO (str): Documento do representante.
        TIPO_DOCUMENTO (str): Tipo do documento.
        REPRESENTADO (str): Nome da parte representada.
        TIPO_PARTE (str): Tipo da parte representada.
        TIPO_PESSOA (str): Tipo da pessoa (física/jurídica).
        PROCESSO (str): Número do processo.
        POLO (str): Polo da parte (ativo/passivo).
        OAB (str): Número da OAB do representante.
        EMAILS (str): E-mails do representante.
        TELEFONE (str): Telefone do representante.

    Returns:
        Representantes: Dicionário tipado com dados do representante.

    """

    ID_PJE: int
    NOME: str
    DOCUMENTO: str
    TIPO_DOCUMENTO: str
    REPRESENTADO: str
    TIPO_PARTE: str
    TIPO_PESSOA: str
    PROCESSO: str
    POLO: str
    OAB: str
    EMAILS: str
    TELEFONE: str


class ExpedienteDocumentoPJe(TypedDict):
    """Defina o dicionário para informações de expediente.

    Args:
        expediente (bool): Indica se é expediente.
        expedienteAberto (bool): Indica expediente aberto.
        hasMandadoDevolucaoPendente (bool): Indica mandado pendente.
        mandadoDistribuido (bool): Indica mandado distribuído.

    """

    expediente: bool
    expedienteAberto: bool
    hasMandadoDevolucaoPendente: bool
    mandadoDistribuido: bool


class DocumentoPJe(TypedDict):
    """Defina o dicionário para os dados de um documento do PJe.

    Args:
        id (int): Identificador do documento.
        idUnicoDocumento (str): Identificador único do documento.
        titulo (str): Título do documento.
        idTipo (int): Identificador do tipo do documento.
        tipo (str): Tipo do documento.
        codigoDocumento (str): Código do documento.
        data (str): Data do documento no formato ISO.
        documento (bool): Indica se é documento principal.
        idUsuario (int): Identificador do usuário responsável.
        especializacoes (int): Código de especializações.
        nomeResponsavel (str): Nome do responsável.
        tipoPolo (str): Tipo de polo processual.
        participacaoProcesso (str): Participação no processo.
        favorito (bool): Indica se é favorito.
        ativo (bool): Indica se está ativo.
        documentoSigiloso (bool): Indica se é sigiloso.
        usuarioInterno (bool): Indica se é usuário interno.
        documentoApreciavel (bool): Indica se é apreciável.
        instancia (str): Instância do processo.
        idSignatario (int): Identificador do signatário.
        nomeSignatario (str): Nome do signatário.
        expediente (bool): Indica se é expediente.
        numeroOrdem (int): Número de ordem.
        codigoInstancia (int): Código da instância.
        pendenciaDocInstanciaOrigem (bool): Pendência na instância de origem.
        papelUsuarioDocumento (str): Papel do usuário no documento.
        infoExpedientes (ExpedienteDocumento): Informações de expedientes.
        copia (bool): Indica se é cópia.
        permiteCooperacaoJudiciaria (bool): Permite cooperação judiciária.
        dataJuntadaFutura (bool): Indica juntada futura.

    """

    id: int
    idUnicoDocumento: str
    titulo: str
    idTipo: int
    tipo: str
    codigoDocumento: str
    data: str
    documento: bool
    idUsuario: int
    especializacoes: int
    nomeResponsavel: str
    anexos: list[DocumentoPJe]
    tipoPolo: str
    participacaoProcesso: str
    favorito: bool
    ativo: bool
    documentoSigiloso: bool
    usuarioInterno: bool
    documentoApreciavel: bool
    instancia: str
    idSignatario: int
    nomeSignatario: str
    expediente: bool
    numeroOrdem: int
    codigoInstancia: int
    pendenciaDocInstanciaOrigem: bool
    papelUsuarioDocumento: str
    infoExpedientes: ExpedienteDocumentoPJe
    copia: bool
    permiteCooperacaoJudiciaria: bool
    dataJuntadaFutura: bool


__all__ = [
    "AssuntoPJe",
    "AudienciaProcessoPJe",
    "DocumentoPJe",
    "ExpedienteDocumentoPJe",
    "PJeCapa",
    "PartePJe",
    "RepresentantePJe",
]
