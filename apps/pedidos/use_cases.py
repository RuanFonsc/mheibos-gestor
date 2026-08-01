from dataclasses import dataclass

from django.db import transaction

from apps.catalogo.models import OperadorGestor
from apps.auditoria.services import registrar_evento
from apps.catalogo.permissions import pode_editar_pedido
from apps.financeiro.services import sincronizar_financeiro_pedido
from apps.pedidos.models import HistoricoStatusPedido, Pedido, StatusPedido


class AlteracaoStatusNegada(Exception):
    """A identidade atual não pode executar a transição solicitada."""


class StatusPedidoInvalido(Exception):
    """O status solicitado não pertence ao contrato vigente do Pedido."""


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

    pedido.status = novo_status
    pedido.save(update_fields=["status", "atualizado_em"])
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
        valores_anteriores={"status": status_anterior},
        valores_posteriores={"status": novo_status},
        metadados={"observacao": observacao} if observacao else {},
    )
    sincronizar_financeiro_pedido(pedido)
    return ResultadoAlteracaoStatus(True, status_anterior, novo_status)
