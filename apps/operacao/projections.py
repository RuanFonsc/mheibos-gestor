from dataclasses import dataclass
from typing import Iterable

from django.db.models import Exists, OuterRef, Prefetch, Q, QuerySet

from apps.pedidos.models import Pedido, StatusPedido

from .models import EstadoProcesso, Processo
from .services import CODIGO_FLUXO_PRODUCAO


@dataclass(frozen=True)
class ProjecaoPedido:
    comercial: str
    financeiro: str
    entrega: str
    operacional: str
    fonte_operacional: str
    bloqueio: str = ""


def queryset_com_projecao(queryset: QuerySet[Pedido]) -> QuerySet[Pedido]:
    processos = Processo.objects.filter(tipo=CODIGO_FLUXO_PRODUCAO).prefetch_related(
        "etapas__responsavel"
    )
    return queryset.prefetch_related(Prefetch("processos", queryset=processos))


def projetar_pedido(pedido: Pedido) -> ProjecaoPedido:
    processos = [
        processo
        for processo in pedido.processos.all()
        if processo.tipo == CODIGO_FLUXO_PRODUCAO
    ]
    processo = processos[0] if processos else None
    if processo is None:
        operacional = pedido.get_status_display()
        fonte = "Compatibilidade legada"
        bloqueio = ""
    else:
        operacional = processo.get_estado_operacional_display()
        fonte = f"{processo.modelo_codigo_snapshot} v{processo.modelo_versao_snapshot}"
        etapa_bloqueada = next(
            (etapa for etapa in processo.etapas.all() if etapa.motivo_bloqueio), None
        )
        bloqueio = etapa_bloqueada.motivo_bloqueio if etapa_bloqueada else ""
    return ProjecaoPedido(
        comercial=pedido.get_estado_comercial_display(),
        financeiro=pedido.estado_financeiro_display,
        entrega=pedido.get_estado_entrega_display(),
        operacional=operacional,
        fonte_operacional=fonte,
        bloqueio=bloqueio,
    )


def projetar_lista(pedidos: Iterable[Pedido]) -> list[Pedido]:
    resultado = list(pedidos)
    for pedido in resultado:
        pedido.projecao = projetar_pedido(pedido)
    return resultado


def queryset_fila_producao(*, prontos: bool = False) -> QuerySet[Pedido]:
    processo_producao = Processo.objects.filter(
        pedido_id=OuterRef("pk"), tipo=CODIGO_FLUXO_PRODUCAO
    )
    pedidos = Pedido.objects.annotate(
        _tem_processo_producao=Exists(processo_producao)
    )
    if prontos:
        filtro = Q(
            processos__tipo=CODIGO_FLUXO_PRODUCAO,
            processos__estado_operacional=EstadoProcesso.CONCLUIDO,
        ) | Q(_tem_processo_producao=False, status=StatusPedido.PRONTO)
    else:
        filtro = Q(
            processos__tipo=CODIGO_FLUXO_PRODUCAO,
            processos__estado_operacional__in=[
                EstadoProcesso.EM_ANDAMENTO,
                EstadoProcesso.BLOQUEADO,
            ],
        ) | Q(_tem_processo_producao=False, status=StatusPedido.EM_PRODUCAO)
    return pedidos.filter(filtro).distinct()
