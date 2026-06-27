from django.db.models import Sum
from django.shortcuts import render

from apps.clientes.models import Cliente
from apps.financeiro.models import LancamentoFinanceiro, StatusLancamento, TipoLancamento
from apps.pedidos.models import Pedido


def home(request):
    receitas = (
        LancamentoFinanceiro.objects.filter(
            tipo=TipoLancamento.RECEITA,
            status=StatusLancamento.REALIZADO,
        ).aggregate(total=Sum("valor"))["total"]
        or 0
    )
    despesas = (
        LancamentoFinanceiro.objects.filter(
            tipo=TipoLancamento.DESPESA,
            status=StatusLancamento.REALIZADO,
        ).aggregate(total=Sum("valor"))["total"]
        or 0
    )
    contexto = {
        "clientes": Cliente.objects.count(),
        "pedidos": Pedido.objects.count(),
        "receitas": receitas,
        "despesas": despesas,
        "lucro": receitas - despesas,
    }
    return render(request, "home.html", contexto)
