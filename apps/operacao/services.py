from django.db import transaction
from django.utils import timezone

from apps.auditoria.services import registrar_evento
from apps.catalogo.models import OperadorGestor
from apps.pedidos.models import Pedido

from .models import EstadoEtapa, EstadoProcesso, EtapaProcesso, ModeloFluxo, Processo

CODIGO_FLUXO_PRODUCAO = "PRODUCAO_PEDIDO"
DEFINICAO_PRODUCAO = [
    {"chave": "PRODUZIR", "nome": "Produzir", "ordem": 1, "obrigatoria": True}
]


class ProcessoEncerrado(Exception):
    """Um processo final exige um caso de uso autorizado de reabertura."""


def modelo_producao_vigente() -> ModeloFluxo:
    modelo, _ = ModeloFluxo.objects.get_or_create(
        codigo=CODIGO_FLUXO_PRODUCAO,
        versao=1,
        defaults={
            "nome": "Producao do Pedido",
            "definicao_etapas": DEFINICAO_PRODUCAO,
        },
    )
    return modelo


@transaction.atomic
def iniciar_producao_pedido(*, pedido: Pedido, operador: OperadorGestor) -> Processo:
    modelo = modelo_producao_vigente()
    agora = timezone.now()
    processo, criado = Processo.objects.get_or_create(
        pedido=pedido,
        tipo=CODIGO_FLUXO_PRODUCAO,
        defaults={
            "objetivo": "Produzir os itens confirmados do Pedido.",
            "resultado_esperado": "Itens produzidos e prontos para entrega.",
            "modelo_fluxo": modelo,
            "modelo_codigo_snapshot": modelo.codigo,
            "modelo_versao_snapshot": modelo.versao,
            "estado_operacional": EstadoProcesso.EM_ANDAMENTO,
            "confirmado_em": agora,
            "iniciado_em": agora,
        },
    )
    if not criado and processo.estado_operacional in {
        EstadoProcesso.CONCLUIDO,
        EstadoProcesso.CANCELADO,
        EstadoProcesso.INVIABILIZADO,
        EstadoProcesso.ABANDONADO,
        EstadoProcesso.SUBSTITUIDO,
    }:
        raise ProcessoEncerrado
    if not criado and processo.estado_operacional == EstadoProcesso.BLOQUEADO:
        from apps.pendencias.models import FormaEncerramentoPendencia
        from apps.pendencias.services import encerrar_pendencia_bloqueio

        etapa = processo.etapas.get(chave="PRODUZIR")
        processo.estado_operacional = EstadoProcesso.EM_ANDAMENTO
        processo.save(update_fields=["estado_operacional", "atualizado_em"])
        etapa.estado = EstadoEtapa.EM_ANDAMENTO
        etapa.motivo_bloqueio = ""
        etapa.save(update_fields=["estado", "motivo_bloqueio"])
        registrar_evento(
            tipo="ProcessoDesbloqueado",
            operador=operador,
            origem="pedidos",
            alvo_tipo="Processo",
            alvo_id=str(processo.pk),
            acao="retomar",
            valores_anteriores={"estado_operacional": EstadoProcesso.BLOQUEADO},
            valores_posteriores={"estado_operacional": processo.estado_operacional},
            metadados={"pedido_id": pedido.pk},
        )
        encerrar_pendencia_bloqueio(
            processo=processo,
            operador=operador,
            forma=FormaEncerramentoPendencia.RESOLUCAO,
        )
        return processo
    if not criado:
        return processo

    etapa = EtapaProcesso.objects.create(
        processo=processo,
        chave="PRODUZIR",
        nome="Produzir",
        ordem=1,
        obrigatoria=True,
        estado=EstadoEtapa.EM_ANDAMENTO,
        responsavel=operador,
        iniciada_em=agora,
    )
    registrar_evento(
        tipo="ProcessoConfirmado",
        operador=operador,
        origem="pedidos",
        alvo_tipo="Processo",
        alvo_id=str(processo.pk),
        acao="confirmar_fluxo",
        valores_anteriores={},
        valores_posteriores={
            "estado_operacional": processo.estado_operacional,
            "modelo": modelo.codigo,
            "versao": modelo.versao,
        },
        metadados={"pedido_id": pedido.pk, "etapa_id": str(etapa.pk)},
    )
    return processo


@transaction.atomic
def concluir_producao_pedido(*, pedido: Pedido, operador: OperadorGestor) -> Processo | None:
    from apps.pendencias.models import FormaEncerramentoPendencia
    from apps.pendencias.services import encerrar_pendencia_bloqueio

    processo = Processo.objects.filter(
        pedido=pedido, tipo=CODIGO_FLUXO_PRODUCAO
    ).first()
    if processo is None:
        return None
    etapa = processo.etapas.get(chave="PRODUZIR")
    if etapa.estado == EstadoEtapa.CONCLUIDA:
        return processo

    agora = timezone.now()
    estado_anterior = etapa.estado
    etapa.estado = EstadoEtapa.CONCLUIDA
    etapa.concluida_por = operador
    etapa.concluida_em = agora
    etapa.motivo_bloqueio = ""
    etapa.save(
        update_fields=["estado", "concluida_por", "concluida_em", "motivo_bloqueio"]
    )
    processo.estado_operacional = EstadoProcesso.CONCLUIDO
    processo.concluido_em = agora
    processo.save(update_fields=["estado_operacional", "concluido_em", "atualizado_em"])
    registrar_evento(
        tipo="EtapaConcluida",
        operador=operador,
        origem="pedidos",
        alvo_tipo="EtapaProcesso",
        alvo_id=str(etapa.pk),
        acao="concluir",
        valores_anteriores={"estado": estado_anterior},
        valores_posteriores={"estado": etapa.estado},
        metadados={"processo_id": str(processo.pk), "pedido_id": pedido.pk},
    )
    encerrar_pendencia_bloqueio(
        processo=processo,
        operador=operador,
        forma=FormaEncerramentoPendencia.RESOLUCAO,
    )
    return processo


@transaction.atomic
def bloquear_producao_pedido(
    *, pedido: Pedido, operador: OperadorGestor, motivo: str
) -> Processo | None:
    from apps.pendencias.services import abrir_pendencia_bloqueio

    processo = Processo.objects.filter(
        pedido=pedido, tipo=CODIGO_FLUXO_PRODUCAO
    ).first()
    if processo is None:
        return None
    etapa = processo.etapas.get(chave="PRODUZIR")
    estado_anterior = etapa.estado
    etapa.estado = EstadoEtapa.BLOQUEADA
    etapa.motivo_bloqueio = motivo
    etapa.save(update_fields=["estado", "motivo_bloqueio"])
    processo.estado_operacional = EstadoProcesso.BLOQUEADO
    processo.save(update_fields=["estado_operacional", "atualizado_em"])
    registrar_evento(
        tipo="ProcessoBloqueado",
        operador=operador,
        origem="pedidos",
        alvo_tipo="Processo",
        alvo_id=str(processo.pk),
        acao="bloquear",
        valores_anteriores={"estado_etapa": estado_anterior},
        valores_posteriores={"estado_operacional": processo.estado_operacional},
        metadados={"motivo": motivo, "pedido_id": pedido.pk},
    )
    abrir_pendencia_bloqueio(
        processo=processo,
        responsavel=etapa.responsavel or operador,
        descricao=motivo,
    )
    return processo


@transaction.atomic
def cancelar_producao_pedido(
    *, pedido: Pedido, operador: OperadorGestor, motivo: str
) -> Processo | None:
    from apps.pendencias.models import FormaEncerramentoPendencia
    from apps.pendencias.services import encerrar_pendencia_bloqueio

    processo = Processo.objects.filter(
        pedido=pedido, tipo=CODIGO_FLUXO_PRODUCAO
    ).first()
    if processo is None or processo.estado_operacional == EstadoProcesso.CANCELADO:
        return processo
    estado_anterior = processo.estado_operacional
    processo.estado_operacional = EstadoProcesso.CANCELADO
    processo.save(update_fields=["estado_operacional", "atualizado_em"])
    processo.etapas.exclude(estado=EstadoEtapa.CONCLUIDA).update(
        estado=EstadoEtapa.CANCELADA
    )
    registrar_evento(
        tipo="ProcessoCancelado",
        operador=operador,
        origem="pedidos",
        alvo_tipo="Processo",
        alvo_id=str(processo.pk),
        acao="cancelar",
        valores_anteriores={"estado_operacional": estado_anterior},
        valores_posteriores={"estado_operacional": processo.estado_operacional},
        metadados={"motivo": motivo, "pedido_id": pedido.pk},
    )
    encerrar_pendencia_bloqueio(
        processo=processo,
        operador=operador,
        forma=FormaEncerramentoPendencia.CANCELAMENTO_AUTORIZADO,
    )
    return processo
