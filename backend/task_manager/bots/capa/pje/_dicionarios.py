from __future__ import annotations

from typing import TypedDict


class ExpedienteDocumento(TypedDict):
    """
    Defina o dicionário para informações de expediente.

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
    """
    Defina o dicionário para os dados de um documento do PJe.

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
    infoExpedientes: ExpedienteDocumento
    copia: bool
    permiteCooperacaoJudiciaria: bool
    dataJuntadaFutura: bool
