from collections import defaultdict
from decimal import Decimal

from django.db.models import Sum
from django.db.models.functions import ExtractMonth, ExtractYear

from apps.financeiro.models import CategoriaFinanceira, LancamentoFinanceiro, StatusLancamento, TipoLancamento

MESES = [
    "Janeiro",
    "Fevereiro",
    "Março",
    "Abril",
    "Maio",
    "Junho",
    "Julho",
    "Agosto",
    "Setembro",
    "Outubro",
    "Novembro",
    "Dezembro",
]
MESES_CURTOS = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]


def _lancamentos_ano(ano):
    return LancamentoFinanceiro.objects.exclude(status=StatusLancamento.CANCELADO).filter(
        data_competencia__year=ano
    )


def _pivot_por_categoria(tipo, ano):
    categorias = list(CategoriaFinanceira.objects.filter(tipo=tipo, ativa=True).order_by("ordem", "nome"))
    valores: defaultdict[int, list[Decimal]] = defaultdict(lambda: [Decimal("0.00")] * 12)
    totais_categoria: defaultdict[int, Decimal] = defaultdict(lambda: Decimal("0.00"))

    agregados = (
        _lancamentos_ano(ano)
        .filter(tipo=tipo)
        .annotate(mes=ExtractMonth("data_competencia"))
        .values("categoria_id", "mes")
        .annotate(total=Sum("valor"))
    )
    for row in agregados:
        if not row["mes"]:
            continue
        mes_idx = row["mes"] - 1
        valores[row["categoria_id"]][mes_idx] = row["total"] or Decimal("0.00")
        totais_categoria[row["categoria_id"]] += row["total"] or Decimal("0.00")

    linhas = []
    total_mensal = [Decimal("0.00")] * 12
    for categoria in categorias:
        meses = valores[categoria.id]
        linhas.append(
            {
                "categoria": categoria,
                "meses": [float(valor) for valor in meses],
                "total": float(totais_categoria[categoria.id]),
            }
        )
        for idx, valor in enumerate(meses):
            total_mensal[idx] += valor

    return {
        "linhas": linhas,
        "total_mensal": [float(valor) for valor in total_mensal],
        "total_anual": float(sum(total_mensal)),
    }


def fluxo_caixa_anual(ano):
    receitas = [Decimal("0.00")] * 12
    despesas = [Decimal("0.00")] * 12

    for row in (
        _lancamentos_ano(ano)
        .annotate(mes=ExtractMonth("data_competencia"))
        .values("tipo", "mes")
        .annotate(total=Sum("valor"))
    ):
        if not row["mes"]:
            continue
        idx = row["mes"] - 1
        if row["tipo"] == TipoLancamento.RECEITA:
            receitas[idx] = row["total"] or Decimal("0.00")
        else:
            despesas[idx] = row["total"] or Decimal("0.00")

    linhas = []
    for idx, nome in enumerate(MESES):
        receita = receitas[idx]
        despesa = despesas[idx]
        linhas.append(
            {
                "mes": nome,
                "mes_curto": MESES_CURTOS[idx],
                "receitas": float(receita),
                "despesas": float(despesa),
                "lucro": float(receita - despesa),
            }
        )

    total_receitas = sum(receitas)
    total_despesas = sum(despesas)
    lucro = total_receitas - total_despesas
    margem = float(lucro / total_receitas * 100) if total_receitas else 0.0
    return {
        "linhas": linhas,
        "total_receitas": float(total_receitas),
        "total_despesas": float(total_despesas),
        "lucro": float(lucro),
        "margem": margem,
    }


def relatorio_crm(ano):
    receitas = _pivot_por_categoria(TipoLancamento.RECEITA, ano)
    despesas = _pivot_por_categoria(TipoLancamento.DESPESA, ano)
    fluxo = fluxo_caixa_anual(ano)
    return {
        "ano": ano,
        "meses": MESES_CURTOS,
        "receitas": receitas,
        "despesas": despesas,
        "fluxo": fluxo,
    }
