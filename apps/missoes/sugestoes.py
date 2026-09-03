from collections import Counter

from django.urls import reverse
from django.utils import timezone

from apps.catalogo.permissions import pode_editar_pedido
from apps.pedidos.models import Pedido, StatusPedido

from .models import EstadoMissao, ReferenciaPedidoMissao


_ESTADOS_ENCERRADOS = {StatusPedido.ENTREGUE, StatusPedido.CANCELADO}
_ESTADOS_MISSAO_ATIVOS = {
    EstadoMissao.PROPOSTA,
    EstadoMissao.AGUARDANDO_ACEITE,
    EstadoMissao.PLANEJADA,
    EstadoMissao.ATIVA,
    EstadoMissao.PAUSADA,
    EstadoMissao.BLOQUEADA,
    EstadoMissao.EM_REVISAO,
}


def pedidos_atrasados_elegiveis(*, operador):
    """Retorna pedidos vencidos que o operador pode acompanhar."""
    if not operador or not operador.ativo:
        return []
    pedidos = Pedido.objects.filter(
        data_entrega__lt=timezone.localdate(),
    ).exclude(status__in=_ESTADOS_ENCERRADOS).select_related("cliente")
    return [
        pedido
        for pedido in pedidos.order_by("data_entrega", "pk")
        if pode_editar_pedido(pedido, operador)
    ]


def proposta_missao_pedidos_atrasados(*, operador):
    """Monta uma proposta segura e não persistente para recuperar atrasos."""
    pedidos = pedidos_atrasados_elegiveis(operador=operador)
    if not pedidos:
        return None

    ids = [pedido.pk for pedido in pedidos]
    ja_cobertos = set(
        ReferenciaPedidoMissao.objects.filter(
            pedido_id__in=ids,
            missao__estado__in=_ESTADOS_MISSAO_ATIVOS,
        ).values_list("pedido_id", flat=True)
    )
    pedidos = [pedido for pedido in pedidos if pedido.pk not in ja_cobertos]
    if not pedidos:
        return None

    hoje = timezone.localdate()
    contagem_status = Counter(pedido.get_status_display() for pedido in pedidos)
    status_resumo = ", ".join(
        f"{quantidade} {status.casefold()}"
        for status, quantidade in contagem_status.most_common(3)
    )
    quantidade = len(pedidos)
    plural = "pedido" if quantidade == 1 else "pedidos"
    maior_atraso = max((hoje - pedido.data_entrega).days for pedido in pedidos)
    amostra = [
        {
            "id": pedido.pk,
            "rotulo": f"Pedido #{pedido.legado_id or pedido.pk}",
            "cliente": pedido.cliente.nome,
            "status": pedido.get_status_display(),
            "data_entrega": pedido.data_entrega.isoformat(),
            "data_entrega_label": pedido.data_entrega.strftime("%d/%m/%Y"),
            "dias_atraso": max(0, (hoje - pedido.data_entrega).days),
            "href": reverse("pedido_detail", args=[pedido.pk]),
        }
        for pedido in pedidos[:6]
    ]
    return {
        "id": "pedidos_atrasados",
        "titulo": "Recuperar pedidos atrasados",
        "motivo": (
            f"{quantidade} {plural} estão com a data de entrega vencida "
            "e ainda não foram concluídos."
        ),
        "resumo": f"Mais antigo: {maior_atraso} dias de atraso · {status_resumo}.",
        "quantidade": quantidade,
        "pedido_ids": [pedido.pk for pedido in pedidos],
        "pedidos": amostra,
        "pedidos_url": f"{reverse('pedido_list')}?atrasados=1",
        "revisar_url": f"{reverse('missao_criar')}?sugestao=pedidos_atrasados",
        "objetivo": (
            "Revisar os pedidos vencidos, priorizar os riscos e registrar uma próxima "
            "ação para cada pedido sem alterar status automaticamente."
        ),
        "criterio_conclusao": (
            "Cada pedido referenciado tem uma próxima ação registrada e foi atualizado, "
            "encaminhado ou conscientemente mantido em acompanhamento."
        ),
        "resultado_esperado": (
            "Fila de atrasos organizada, bloqueios visíveis e decisões registradas "
            "sem perder o histórico oficial dos pedidos."
        ),
    }
