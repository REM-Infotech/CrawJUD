"""Dicionários TypedDict usados para mapear movimentações e documentos do PJe.

Este módulo fornece definições de TypedDict para estrutura de dados
retornadas pelo sistema PJe: DocumentoPJe, ExpedienteDocumentoPJe e
MovimentacaoPJe.
"""

from __future__ import annotations

from typing import TypedDict


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


class MovimentacaoPJe(TypedDict):
    """Defina o dicionário para os dados de uma movimentação do PJe.

    Campos:
        id (int): Identificador da movimentação.
        processo (str): Identificador ou número do processo.
        titulo (str): Título ou descrição da movimentação.
        data (str): Data da movimentação no formato ISO.
        documento (bool): Indica se há documento associado à movimentação.
        idUsuario (int): Identificador do usuário responsável.
        especializacoes (int): Código de especializações.
        nomeResponsavel (str): Nome do responsável pela movimentação.
        tipoPolo (str): Tipo de polo processual.
        favorito (bool): Indica se está marcado como favorito.
        ativo (bool): Indica se a movimentação está ativa.
        documentoSigiloso (bool): Indica se o documento é sigiloso.
        usuarioInterno (bool): Indica se o usuário é interno.
        documentoApreciavel (bool): Indica se o documento é apreciável.
        expediente (bool): Indica se é expediente.
        numeroOrdem (int): Número de ordem da movimentação.
        codigoInstancia (int): Código da instância processual.
        pendenciaDocInstanciaOrigem (bool): Pendência na instância de origem.
        copia (bool): Indica se é cópia.
        codigoMovimentoCNJ (int): Código do movimento conforme CNJ.
        permiteCooperacaoJudiciaria (bool): Permite cooperação judiciária.
        movimentoPermiteExclusao (bool): Indica se permite exclusão.
        movimentoPermiteRetificacao (bool): Indica se permite retificação.
        movimentoFoiRetificado (bool): Indica se já foi retificado.
        dataJuntadaFutura (bool): Indica juntada futura.
    """

    id: int
    processo: str
    titulo: str
    data: str
    documento: bool
    idUsuario: int
    especializacoes: int
    nomeResponsavel: str
    tipoPolo: str
    favorito: bool
    ativo: bool
    documentoSigiloso: bool
    usuarioInterno: bool
    documentoApreciavel: bool
    expediente: bool
    numeroOrdem: int
    codigoInstancia: int
    pendenciaDocInstanciaOrigem: bool
    copia: bool
    codigoMovimentoCNJ: int
    permiteCooperacaoJudiciaria: bool
    movimentoPermiteExclusao: bool
    movimentoPermiteRetificacao: bool
    movimentoFoiRetificado: bool
    dataJuntadaFutura: bool


__all__ = ["DocumentoPJe", "ExpedienteDocumentoPJe", "MovimentacaoPJe"]
