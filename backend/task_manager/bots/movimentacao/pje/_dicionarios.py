from __future__ import annotations

from typing import TypedDict


class PJeMovimentacao(TypedDict):
    NUMERO_PROCESSO: str
    GRAU: str
    REGIAO: str


class ExpedienteDocumento(TypedDict):
    expediente: bool
    expedienteAberto: bool
    hasMandadoDevolucaoPendente: bool
    mandadoDistribuido: bool


class DocumentoPJe(TypedDict):
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
