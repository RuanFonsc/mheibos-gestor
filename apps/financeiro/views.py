from decimal import Decimal

from django.contrib import messages
from django.db.models import Count, DecimalField, ExpressionWrapper, F, Sum
from django.db.models.functions import ExtractMonth
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from apps.financeiro.crm import MESES_CURTOS, relatorio_crm
from apps.financeiro.forms import LancamentoCRMForm
from apps.financeiro.models import CategoriaFinanceira, LancamentoFinanceiro, StatusLancamento, TipoLancamento
from apps.financeiro.services import garantir_categorias_financeiras
from apps.catalogo.permissions import operador_atual
from apps.pedidos.models import Pedido, PedidoItem, StatusPedido


def dashboard(request):
    garantir_categorias_financeiras()
    operador = operador_atual()
    aba = request.GET.get("aba", "dashboard")
    if aba not in {"dashboard", "crm"}:
        aba = "dashboard"
    escopo = request.GET.get("escopo", "pessoal")
    if escopo == "geral" and not operador.is_admin:
        escopo = "pessoal"

    ano = timezone.localdate().year
    try:
        ano = int(request.GET.get("ano", ano))
    except (TypeError, ValueError):
        pass

    if request.method == "POST":
        acao = request.POST.get("acao")
        if acao == "criar_lancamento":
            form = LancamentoCRMForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Lançamento registrado no CRM.")
            else:
                messages.error(request, f"Não foi possível salvar: {form.errors.as_text()}")
            return redirect(f"{request.path}?aba=crm&ano={ano}")
        if acao == "excluir_lancamento":
            lancamento = get_object_or_404(LancamentoFinanceiro, pk=request.POST.get("lancamento_id"))
            if lancamento.pedido_id and lancamento.pagamento_pedido_id:
                messages.error(request, "Lançamentos gerados por pedidos não podem ser excluídos aqui.")
            else:
                lancamento.status = StatusLancamento.CANCELADO
                lancamento.save(update_fields=["status", "atualizado_em"])
                messages.success(request, "Lançamento removido.")
            return redirect(f"{request.path}?aba=crm&ano={ano}")

    pedidos_validos = Pedido.objects.exclude(status=StatusPedido.CANCELADO)
    if escopo != "geral":
        pedidos_validos = pedidos_validos.filter(usuario_cadastro__iexact=operador.nome)
    pedidos_validos = pedidos_validos.select_related("cliente")
    pedidos_ids = pedidos_validos.values("id")
    receita_total = (
        LancamentoFinanceiro.objects.filter(tipo=TipoLancamento.RECEITA, pedido_id__in=pedidos_ids)
        .exclude(status=StatusLancamento.CANCELADO)
        .aggregate(total=Sum("valor"))["total"]
        or Decimal("0.00")
    )
    if receita_total == Decimal("0.00"):
        receita_total = pedidos_validos.aggregate(total=Sum("valor_total"))["total"] or Decimal("0.00")
    despesa_total = (
        LancamentoFinanceiro.objects.filter(tipo=TipoLancamento.DESPESA, status=StatusLancamento.REALIZADO)
        .aggregate(total=Sum("valor"))["total"]
        or Decimal("0.00")
    ) if escopo == "geral" else Decimal("0.00")
    custo_producao = (
        PedidoItem.objects.filter(pedido_id__in=pedidos_ids).aggregate(
            total=Sum(
                ExpressionWrapper(
                    F("quantidade") * F("custo_unitario_estimado"),
                    output_field=DecimalField(max_digits=12, decimal_places=2),
                )
            )
        )["total"]
        or Decimal("0.00")
    )
    lucro_real = receita_total - despesa_total - custo_producao
    margem = (lucro_real / receita_total * 100) if receita_total else Decimal("0.00")
    total_pedidos = pedidos_validos.count()
    ticket = pedidos_validos.aggregate(avg=Sum("valor_total"))["avg"] or Decimal("0.00")
    ticket_medio = ticket / total_pedidos if total_pedidos else Decimal("0.00")

    receita_mensal = [0] * 12
    despesa_mensal = [0] * 12
    receita_agregada = (
        pedidos_validos.filter(data_pedido__year=ano)
        .annotate(mes=ExtractMonth("data_pedido"))
        .values("mes")
        .annotate(total=Sum("valor_total"))
    )
    for row in receita_agregada:
        if not row["mes"]:
            continue
        receita_mensal[row["mes"] - 1] = float(row["total"] or 0)
    if escopo == "geral":
        for row in (
            LancamentoFinanceiro.objects.exclude(status=StatusLancamento.CANCELADO)
            .filter(data_competencia__year=ano, tipo=TipoLancamento.DESPESA)
            .annotate(mes=ExtractMonth("data_competencia"))
            .values("mes")
            .annotate(total=Sum("valor"))
        ):
            if not row["mes"]:
                continue
            despesa_mensal[row["mes"] - 1] = float(row["total"] or 0)

    status_rows = pedidos_validos.values("status").annotate(total=Count("id")).order_by("-total")
    top_produtos = (
        PedidoItem.objects.filter(pedido_id__in=pedidos_ids).values("nome")
        .annotate(quantidade=Count("id"), faturamento=Sum("preco_unitario"))
        .order_by("-quantidade")[:5]
    )

    hoje = timezone.localdate()
    inicio_mes = hoje.replace(day=1)
    data_inicio_txt = request.GET.get("inicio") or ""
    data_fim_txt = request.GET.get("fim") or ""
    periodo_inicio = inicio_mes
    periodo_fim = hoje
    try:
        if data_inicio_txt:
            periodo_inicio = timezone.datetime.fromisoformat(data_inicio_txt).date()
        if data_fim_txt:
            periodo_fim = timezone.datetime.fromisoformat(data_fim_txt).date()
    except ValueError:
        periodo_inicio, periodo_fim = inicio_mes, hoje
    vendas_periodo = pedidos_validos.filter(data_pedido__range=(periodo_inicio, periodo_fim)).order_by("-data_pedido", "-id")
    vendas_dia = pedidos_validos.filter(data_pedido=hoje)
    vendas_mes = pedidos_validos.filter(data_pedido__range=(inicio_mes, hoje))

    crm = relatorio_crm(ano)
    lancamento_form = LancamentoCRMForm(
        initial={
            "tipo": TipoLancamento.DESPESA,
            "data_competencia": timezone.localdate(),
            "status": StatusLancamento.REALIZADO,
        }
    )
    lancamentos_recentes = (
        LancamentoFinanceiro.objects.select_related("categoria", "pedido")
        .exclude(status=StatusLancamento.CANCELADO)
        .filter(data_competencia__year=ano)
        .order_by("-data_competencia", "-id")[:20]
    )
    anos_disponiveis = list(range(timezone.localdate().year, timezone.localdate().year - 5, -1))

    contexto = {
        "active": "dashboard",
        "aba": aba,
        "escopo": escopo,
        "operador_atual": operador,
        "pode_ver_geral": operador.is_admin,
        "ano": ano,
        "anos_disponiveis": anos_disponiveis,
        "receita_total": receita_total,
        "despesa_total": despesa_total,
        "lucro": lucro_real,
        "custo_producao": custo_producao,
        "margem": margem,
        "total_pedidos": total_pedidos,
        "em_producao": pedidos_validos.filter(status__in=[StatusPedido.EM_PRODUCAO, StatusPedido.AGUARDANDO_ARTE]).count(),
        "ticket_medio": ticket_medio,
        "vendas_dia_total": vendas_dia.aggregate(total=Sum("valor_total"))["total"] or Decimal("0.00"),
        "vendas_dia_count": vendas_dia.count(),
        "vendas_mes_total": vendas_mes.aggregate(total=Sum("valor_total"))["total"] or Decimal("0.00"),
        "vendas_mes_count": vendas_mes.count(),
        "periodo_inicio": periodo_inicio,
        "periodo_fim": periodo_fim,
        "vendas_periodo": vendas_periodo[:80],
        "vendas_periodo_total": vendas_periodo.aggregate(total=Sum("valor_total"))["total"] or Decimal("0.00"),
        "meses": MESES_CURTOS,
        "receita_mensal": receita_mensal,
        "despesa_mensal": despesa_mensal,
        "status_rows": status_rows,
        "top_produtos": top_produtos,
        "crm": crm,
        "lancamento_form": lancamento_form,
        "lancamentos_recentes": lancamentos_recentes,
        "categorias_receita": CategoriaFinanceira.objects.filter(tipo=TipoLancamento.RECEITA, ativa=True),
        "categorias_despesa": CategoriaFinanceira.objects.filter(tipo=TipoLancamento.DESPESA, ativa=True),
    }
    return render(request, "financeiro/dashboard.html", contexto)
