from dataclasses import dataclass

from django.db import transaction

from apps.catalogo.models import OperadorGestor
from apps.auditoria.services import registrar_evento
from apps.catalogo.permissions import pode_editar_pedido
from apps.financeiro.services import sincronizar_financeiro_pedido
from apps.operacao.services import (
    bloquear_producao_pedido,
    cancelar_producao_pedido,
    concluir_producao_pedido,
    iniciar_producao_pedido,
)
from apps.pedidos.models import (
    EstadoComercialPedido,
    EstadoEntregaPedido,
    HistoricoStatusPedido,
    Pedido,
    StatusPedido,
)


class AlteracaoStatusNegada(Exception):
    """A identidade atual não pode executar a transição solicitada."""


class StatusPedidoInvalido(Exception):
    """O status solicitado não pertence ao contrato vigente do Pedido."""


class EntregaComSaldoNegada(Exception):
    """Entrega com saldo exige autorizacao superior explicita."""


@dataclass(frozen=True)
class ResultadoAlteracaoStatus:
    alterado: bool
    status_anterior: str
    status_novo: str


@transaction.atomic
def alterar_status_pedido(
    *,
    pedido: Pedido,
    novo_status: str,
    operador: OperadorGestor,
    origem_operacional: bool = False,
    observacao: str = "",
) -> ResultadoAlteracaoStatus:
    valores_validos = {valor for valor, _rotulo in StatusPedido.choices}
    if novo_status not in valores_validos:
        raise StatusPedidoInvalido(novo_status)

    status_anterior = pedido.status
    if novo_status == status_anterior:
        return ResultadoAlteracaoStatus(False, status_anterior, novo_status)

    if novo_status == StatusPedido.CANCELADO:
        permitido = operador.pode_cancelar_pedido
    else:
        permitido = origem_operacional or pode_editar_pedido(pedido, operador)
    if not permitido:
        raise AlteracaoStatusNegada

    if novo_status == StatusPedido.ENTREGUE and pedido.saldo_aberto > 0:
        raise EntregaComSaldoNegada

    comercial_anterior = pedido.estado_comercial
    entrega_anterior = pedido.estado_entrega
    pedido.status = novo_status
    if novo_status == StatusPedido.CANCELADO:
        pedido.estado_comercial = EstadoComercialPedido.CANCELADO
    elif novo_status == StatusPedido.ENTREGUE:
        pedido.estado_entrega = EstadoEntregaPedido.ENTREGUE
        pedido.estado_comercial = EstadoComercialPedido.CONCLUIDO
    elif novo_status == StatusPedido.PRONTO:
        pedido.estado_entrega = EstadoEntregaPedido.PRONTO
    pedido.save(
        update_fields=["status", "estado_comercial", "estado_entrega", "atualizado_em"]
    )
    HistoricoStatusPedido.objects.create(
        pedido=pedido,
        status_anterior=status_anterior,
        status_novo=novo_status,
        observacao=observacao,
        operador=operador,
    )
    registrar_evento(
        tipo="PedidoStatusAlterado",
        operador=operador,
        origem="pedidos",
        alvo_tipo="Pedido",
        alvo_id=str(pedido.pk),
        acao="alterar_status",
        valores_anteriores={
            "status_legado": status_anterior,
            "estado_comercial": comercial_anterior,
            "estado_entrega": entrega_anterior,
        },
        valores_posteriores={
            "status_legado": novo_status,
            "estado_comercial": pedido.estado_comercial,
            "estado_entrega": pedido.estado_entrega,
        },
        metadados={"observacao": observacao} if observacao else {},
    )
    if novo_status == StatusPedido.EM_PRODUCAO:
        iniciar_producao_pedido(pedido=pedido, operador=operador)
    elif novo_status == StatusPedido.PRONTO:
        concluir_producao_pedido(pedido=pedido, operador=operador)
    elif novo_status == StatusPedido.CANCELADO:
        cancelar_producao_pedido(
            pedido=pedido, operador=operador, motivo=observacao
        )
    elif status_anterior == StatusPedido.EM_PRODUCAO and observacao:
        bloquear_producao_pedido(
            pedido=pedido, operador=operador, motivo=observacao
        )
    sincronizar_financeiro_pedido(pedido)
    return ResultadoAlteracaoStatus(True, status_anterior, novo_status)
