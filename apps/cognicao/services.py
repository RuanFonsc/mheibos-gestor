from apps.operacao.projections import projetar_pedido
from apps.pedidos.models import Pedido

from .gateway import GatewayIA, RespostaCognitiva, SolicitacaoCognitiva


def resumir_pedido(*, pedido: Pedido, gateway: GatewayIA) -> RespostaCognitiva:
    projecao = projetar_pedido(pedido)
    contexto = "\n".join(
        [
            f"Pedido tecnico: {pedido.pk}",
            f"Estado comercial: {projecao.comercial}",
            f"Estado financeiro: {projecao.financeiro}",
            f"Estado de entrega: {projecao.entrega}",
            f"Estado operacional: {projecao.operacional}",
            f"Fonte operacional: {projecao.fonte_operacional}",
            f"Bloqueio registrado: {projecao.bloqueio or 'nenhum'}",
        ]
    )
    return gateway.solicitar(
        SolicitacaoCognitiva(capacidade="resumo_operacional_pedido", contexto=contexto)
    )
