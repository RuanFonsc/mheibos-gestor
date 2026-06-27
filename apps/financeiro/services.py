from decimal import Decimal

from django.db import transaction
from django.utils import timezone

from apps.financeiro.models import (
    CategoriaFinanceira,
    ContaFinanceira,
    GrupoFinanceiro,
    LancamentoFinanceiro,
    StatusLancamento,
    TipoLancamento,
)
from apps.pedidos.models import PagamentoPedido, StatusPagamento, StatusPedido


CATEGORIA_VENDAS_PEDIDOS = "Vendas de pedidos"

def garantir_categorias_financeiras():
    from apps.financeiro.management.commands.preparar_financeiro import CATEGORIAS

    for nome, tipo, grupo, ordem in CATEGORIAS:
        CategoriaFinanceira.objects.get_or_create(
            nome=nome,
            tipo=tipo,
            defaults={"grupo": grupo, "ordem": ordem},
        )
    ContaFinanceira.objects.get_or_create(nome="Caixa principal")


def obter_categoria_vendas_pedidos():
    categoria, _ = CategoriaFinanceira.objects.get_or_create(
        nome=CATEGORIA_VENDAS_PEDIDOS,
        tipo=TipoLancamento.RECEITA,
        defaults={"grupo": GrupoFinanceiro.VENDAS, "ordem": 10},
    )
    return categoria


@transaction.atomic
def sincronizar_financeiro_pedido(pedido):
    if pedido.status == StatusPedido.CANCELADO:
        LancamentoFinanceiro.objects.filter(pedido=pedido).update(
            status=StatusLancamento.CANCELADO
        )
        return

    categoria = obter_categoria_vendas_pedidos()
    pagamentos = pedido.pagamentos.filter(status=StatusPagamento.CONFIRMADO)

    for pagamento in pagamentos:
        data_competencia = pedido.data_pedido or pagamento.data_pagamento or timezone.localdate()
        LancamentoFinanceiro.objects.update_or_create(
            pagamento_pedido=pagamento,
            defaults={
                "tipo": TipoLancamento.RECEITA,
                "categoria": categoria,
                "pedido": pedido,
                "descricao": f"Recebimento do pedido #{pedido.pk}",
                "valor": pagamento.valor,
                "data_competencia": data_competencia,
                "data_vencimento": pagamento.data_pagamento,
                "data_pagamento": pagamento.data_pagamento,
                "status": StatusLancamento.REALIZADO,
            },
        )

    total_pago = pagamentos.aggregate_total() if hasattr(pagamentos, "aggregate_total") else None
    if total_pago is None:
        from django.db.models import Sum

        total_pago = pagamentos.aggregate(soma=Sum("valor"))["soma"] or Decimal("0.00")

    saldo = pedido.valor_total - total_pago
    LancamentoFinanceiro.objects.filter(
        pedido=pedido,
        pagamento_pedido__isnull=True,
        descricao__startswith="Saldo previsto",
    ).delete()

    if saldo > Decimal("0.00"):
        data_competencia = pedido.data_pedido or pedido.data_entrega or timezone.localdate()
        LancamentoFinanceiro.objects.create(
            tipo=TipoLancamento.RECEITA,
            categoria=categoria,
            pedido=pedido,
            descricao=f"Saldo previsto do pedido #{pedido.pk}",
            valor=saldo,
            data_competencia=data_competencia,
            data_vencimento=pedido.data_entrega or data_competencia,
            status=StatusLancamento.PREVISTO,
        )
