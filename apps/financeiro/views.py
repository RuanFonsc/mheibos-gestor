from decimal import Decimal
from datetime import datetime, timedelta
from io import BytesIO

from django.contrib import messages
from django.db.models import Count, DecimalField, ExpressionWrapper, F, Sum
from django.db.models.functions import ExtractMonth
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from reportlab.lib import colors
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.shapes import Drawing
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from apps.financeiro.crm import MESES_CURTOS, relatorio_crm
from apps.financeiro.forms import LancamentoCRMForm
from apps.financeiro.models import CategoriaFinanceira, LancamentoFinanceiro, MetaVendasUsuario, StatusLancamento, TipoLancamento
from apps.financeiro.services import garantir_categorias_financeiras
from apps.catalogo.models import CategoriaUsuario, OperadorGestor
from apps.catalogo.permissions import operador_atual
from apps.pedidos.models import CanalAtendimentoPedido, Pedido, PedidoItem, StatusPedido


def dashboard(request):
    garantir_categorias_financeiras()
    operador = operador_atual(request)
    aba = request.GET.get("aba", "dashboard")
    if aba not in {"dashboard", "relatorios", "crm", "metas"}:
        aba = "dashboard"
    if aba == "metas" and not operador.is_admin_geral:
        aba = "dashboard"
    escopo = request.GET.get("escopo", "pessoal")
    if escopo == "geral" and not operador.is_admin:
        escopo = "pessoal"

    ano = timezone.localdate().year
    try:
        ano = int(request.GET.get("ano", ano))
    except (TypeError, ValueError):
        pass
    hoje = timezone.localdate()
    inicio_mes = hoje.replace(day=1)
    data_inicio_txt = request.GET.get("inicio") or ""
    data_fim_txt = request.GET.get("fim") or ""
    periodo_inicio = inicio_mes
    periodo_fim = hoje
    periodo_manual = bool(data_inicio_txt or data_fim_txt)
    try:
        if data_inicio_txt:
            periodo_inicio = datetime.fromisoformat(data_inicio_txt).date()
        if data_fim_txt:
            periodo_fim = datetime.fromisoformat(data_fim_txt).date()
    except ValueError:
        periodo_inicio, periodo_fim = inicio_mes, hoje
    if periodo_inicio > periodo_fim:
        periodo_inicio, periodo_fim = periodo_fim, periodo_inicio
    meta_usuario, _ = MetaVendasUsuario.objects.get_or_create(
        operador=operador,
        ano=inicio_mes.year,
        mes=inicio_mes.month,
        defaults={"valor": Decimal("0.00")},
    )
    if request.method == "POST":
        acao = request.POST.get("acao")
        if acao == "salvar_meta":
            messages.error(request, "Metas de usuarios devem ser definidas nas configuracoes por um administrador.")
            return redirect(f"{request.path}?aba=dashboard&ano={ano}&escopo=pessoal")
        if acao == "salvar_metas_usuarios":
            if not operador.is_admin_geral:
                raise PermissionDenied("Somente administradores gerais definem metas.")
            operador_ids = request.POST.getlist("meta_operador_ids")
            categoria_redirect = request.POST.get("categoria_usuario") or ""
            if not operador_ids:
                messages.error(request, "Selecione pelo menos um usuario para salvar a meta.")
                return redirect(f"{request.path}?aba=metas&ano={ano}&categoria_usuario={categoria_redirect}")
            salvos = 0
            for usuario_meta in OperadorGestor.objects.filter(pk__in=operador_ids, ativo=True):
                valor_txt = (request.POST.get(f"meta_valor_{usuario_meta.pk}") or "0").strip()
                if "," in valor_txt and "." in valor_txt:
                    valor_txt = valor_txt.replace(".", "").replace(",", ".")
                elif "," in valor_txt:
                    valor_txt = valor_txt.replace(",", ".")
                try:
                    valor = max(Decimal("0.00"), Decimal(valor_txt or "0"))
                except (ValueError, ArithmeticError):
                    messages.error(request, f"Meta invalida para {usuario_meta.nome}.")
                    return redirect(f"{request.path}?aba=metas&ano={ano}&categoria_usuario={categoria_redirect}")
                MetaVendasUsuario.objects.update_or_create(
                    operador=usuario_meta,
                    ano=inicio_mes.year,
                    mes=inicio_mes.month,
                    defaults={"valor": valor},
                )
                salvos += 1
            messages.success(request, f"Metas atualizadas para {salvos} usuario(s).")
            return redirect(f"{request.path}?aba=metas&ano={ano}&categoria_usuario={categoria_redirect}")
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
    if periodo_manual:
        pedidos_validos = pedidos_validos.filter(data_pedido__range=(periodo_inicio, periodo_fim))
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
    vendas_dia = pedidos_validos.filter(data_pedido=hoje)
    vendas_mes = pedidos_validos.filter(data_pedido__range=(inicio_mes, hoje))

    receita_mensal = [0] * 12
    despesa_mensal = [0] * 12
    top_produtos_ranking = []
    top_categorias_ranking = []
    canais_ranking = []
    vendedores_ranking = []
    vendedores_fotos_lista = []
    vendas_hoje_labels = []
    vendas_hoje_valores = []
    if aba == "dashboard":
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

        top_produtos = (
            PedidoItem.objects.filter(pedido_id__in=pedidos_ids)
            .annotate(
                linha_total=ExpressionWrapper(
                    F("quantidade") * F("preco_unitario"),
                    output_field=DecimalField(max_digits=12, decimal_places=2),
                )
            )
            .values("nome")
            .annotate(
                quantidade=Sum("quantidade"),
                faturamento=Sum("linha_total"),
            )
            .order_by("-quantidade")[:6]
        )
        top_categorias = (
            PedidoItem.objects.filter(pedido_id__in=pedidos_ids)
            .annotate(
                linha_total=ExpressionWrapper(
                    F("quantidade") * F("preco_unitario"),
                    output_field=DecimalField(max_digits=12, decimal_places=2),
                )
            )
            .values("categoria_servico__nome")
            .annotate(
                quantidade=Sum("quantidade"),
                faturamento=Sum("linha_total"),
            )
            .order_by("-faturamento", "-quantidade")[:6]
        )
        vendedores_ranking = list(
            Pedido.objects.exclude(status=StatusPedido.CANCELADO)
            .filter(data_pedido__year=ano)
            .exclude(usuario_cadastro="")
            .values("usuario_cadastro")
            .annotate(total=Sum("valor_total"), pedidos=Count("id"))
            .order_by("-total")[:6]
        )
        vendedores_fotos = {
            operador.nome.casefold(): operador.foto.url if operador.foto else ""
            for operador in OperadorGestor.objects.filter(nome__in=[row["usuario_cadastro"] for row in vendedores_ranking])
        }
        vendedores_fotos_lista = [vendedores_fotos.get((row["usuario_cadastro"] or "").casefold(), "") for row in vendedores_ranking]
        top_produtos_ranking = list(top_produtos)
        top_categorias_ranking = list(top_categorias)
        canal_labels = dict(CanalAtendimentoPedido.choices)
        canais_ranking = [
            {
                "canal": row["canal_atendimento"],
                "label": canal_labels.get(row["canal_atendimento"], row["canal_atendimento"] or "Nao informado"),
                "total": row["total"] or Decimal("0.00"),
                "pedidos": row["pedidos"],
            }
            for row in pedidos_validos.values("canal_atendimento").annotate(
                total=Sum("valor_total"),
                pedidos=Count("id"),
            ).order_by("-total")
        ]
        vendas_hoje_labels = [f"{hora:02d}h" for hora in range(8, 19)]
        vendas_hoje_valores = [
            float(vendas_dia.filter(criado_em__hour=hora).aggregate(total=Sum("valor_total"))["total"] or 0)
            for hora in range(8, 19)
        ]

    vendas_periodo = None
    vendas_periodo_total = Decimal("0.00")
    if aba == "relatorios":
        vendas_periodo_qs = pedidos_validos.filter(data_pedido__range=(periodo_inicio, periodo_fim)).order_by("-data_pedido", "-id")
        vendas_periodo = Paginator(vendas_periodo_qs, 20).get_page(request.GET.get("pagina") or 1)
        vendas_periodo_total = vendas_periodo_qs.aggregate(total=Sum("valor_total"))["total"] or Decimal("0.00")
    vendas_mes_total = vendas_mes.aggregate(total=Sum("valor_total"))["total"] or Decimal("0.00")
    mes_anterior_fim = inicio_mes - timedelta(days=1)
    mes_anterior_inicio = mes_anterior_fim.replace(day=1)
    vendas_mes_anterior_total = (
        pedidos_validos.filter(data_pedido__range=(mes_anterior_inicio, mes_anterior_fim)).aggregate(total=Sum("valor_total"))["total"]
        or Decimal("0.00")
    )
    crescimento_mes = (
        ((vendas_mes_total - vendas_mes_anterior_total) / vendas_mes_anterior_total) * 100
        if vendas_mes_anterior_total
        else Decimal("0.00")
    )
    progresso_meta = (vendas_mes_total / meta_usuario.valor * 100) if meta_usuario.valor else Decimal("0.00")
    falta_meta = max(Decimal("0.00"), meta_usuario.valor - vendas_mes_total)

    tipo_relatorio = request.GET.get("relatorio")
    if tipo_relatorio == "dia" and aba == "relatorios":
        vendas_dia_relatorio = pedidos_validos.filter(data_pedido=periodo_inicio)
        return relatorio_vendas_dia_pdf(vendas_dia_relatorio, periodo_inicio, operador, escopo)
    if tipo_relatorio == "mes" and aba == "relatorios":
        return relatorio_vendas_mes_pdf(pedidos_validos, periodo_inicio, operador, escopo)
    if tipo_relatorio == "crm_geral" and aba == "relatorios":
        if not operador.is_admin_geral:
            raise PermissionDenied("Apenas administradores gerais podem gerar o relatorio geral.")
        return relatorio_crm_geral_pdf(relatorio_crm(ano), ano)

    crm = None
    lancamento_form = None
    lancamentos_recentes = []
    categorias_receita = []
    categorias_despesa = []
    if aba == "crm":
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
        categorias_receita = CategoriaFinanceira.objects.filter(tipo=TipoLancamento.RECEITA, ativa=True)
        categorias_despesa = CategoriaFinanceira.objects.filter(tipo=TipoLancamento.DESPESA, ativa=True)
    categorias_usuario = CategoriaUsuario.objects.filter(ativa=True).order_by("ordem", "nome")
    categoria_usuario_atual = request.GET.get("categoria_usuario", "").strip()
    metas_usuarios = []
    metas_labels = []
    metas_valores = []
    metas_realizado_valores = []
    metas_fotos = []
    meta_geral_total = Decimal("0.00")
    meta_geral_realizado = Decimal("0.00")
    meta_geral_progresso = Decimal("0.00")
    meta_geral_falta = Decimal("0.00")
    if aba == "metas":
        usuarios_meta_qs = OperadorGestor.objects.select_related("categoria_usuario").filter(ativo=True).order_by("nome")
        if categoria_usuario_atual.isdigit():
            usuarios_meta_qs = usuarios_meta_qs.filter(categoria_usuario_id=int(categoria_usuario_atual))
        usuarios_meta = list(usuarios_meta_qs)
        metas_mes = {
            meta.operador_id: meta
            for meta in MetaVendasUsuario.objects.filter(
                ano=inicio_mes.year,
                mes=inicio_mes.month,
                operador__in=usuarios_meta,
            )
        }
        vendas_por_nome = {
            (row["usuario_cadastro"] or "").casefold(): row["total"] or Decimal("0.00")
            for row in Pedido.objects.exclude(status=StatusPedido.CANCELADO)
            .filter(data_pedido__range=(inicio_mes, hoje))
            .exclude(usuario_cadastro="")
            .values("usuario_cadastro")
            .annotate(total=Sum("valor_total"))
        }
        for usuario_meta in usuarios_meta:
            meta = metas_mes.get(usuario_meta.pk)
            valor_meta = meta.valor if meta else Decimal("0.00")
            realizado = vendas_por_nome.get(usuario_meta.nome.casefold(), Decimal("0.00"))
            progresso = (realizado / valor_meta * 100) if valor_meta else Decimal("0.00")
            metas_usuarios.append(
                {
                    "operador": usuario_meta,
                    "meta": meta,
                    "valor_meta": valor_meta,
                    "realizado": realizado,
                    "progresso": progresso,
                    "falta": max(Decimal("0.00"), valor_meta - realizado),
                }
            )
            metas_labels.append(usuario_meta.nome)
            metas_valores.append(float(valor_meta))
            metas_realizado_valores.append(float(realizado))
            metas_fotos.append(usuario_meta.foto.url if usuario_meta.foto else "")
        meta_geral_total = sum((item["valor_meta"] for item in metas_usuarios), Decimal("0.00"))
        meta_geral_realizado = sum((item["realizado"] for item in metas_usuarios), Decimal("0.00"))
        meta_geral_progresso = (meta_geral_realizado / meta_geral_total * 100) if meta_geral_total else Decimal("0.00")
        meta_geral_falta = max(Decimal("0.00"), meta_geral_total - meta_geral_realizado)
    anos_disponiveis = list(range(timezone.localdate().year, timezone.localdate().year - 5, -1))

    contexto = {
        "active": "dashboard",
        "aba": aba,
        "escopo": escopo,
        "operador_atual": operador,
        "pode_ver_geral": operador.is_admin,
        "pode_relatorio_geral": operador.is_admin_geral,
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
        "vendas_mes_total": vendas_mes_total,
        "vendas_mes_count": vendas_mes.count(),
        "vendas_mes_anterior_total": vendas_mes_anterior_total,
        "crescimento_mes": crescimento_mes,
        "meta_usuario": meta_usuario,
        "progresso_meta": progresso_meta,
        "falta_meta": falta_meta,
        "periodo_inicio": periodo_inicio,
        "periodo_fim": periodo_fim,
        "vendas_periodo": vendas_periodo,
        "vendas_periodo_total": vendas_periodo_total,
        "meses": MESES_CURTOS,
        "receita_mensal": receita_mensal,
        "despesa_mensal": despesa_mensal,
        "top_produtos": top_produtos_ranking,
        "top_produtos_ranking": top_produtos_ranking,
        "top_categorias_ranking": top_categorias_ranking,
        "canais_ranking": canais_ranking,
        "vendedores_ranking": vendedores_ranking,
        "vendedores_labels": [row["usuario_cadastro"] for row in vendedores_ranking],
        "vendedores_valores": [float(row["total"] or 0) for row in vendedores_ranking],
        "vendedores_fotos": vendedores_fotos_lista,
        "produtos_labels": [row["nome"] for row in top_produtos_ranking],
        "produtos_valores": [float(row["quantidade"] or 0) for row in top_produtos_ranking],
        "categorias_labels": [row["categoria_servico__nome"] or "Sem categoria" for row in top_categorias_ranking],
        "categorias_valores": [float(row["faturamento"] or 0) for row in top_categorias_ranking],
        "canais_labels": [row["label"] for row in canais_ranking],
        "canais_valores": [float(row["total"] or 0) for row in canais_ranking],
        "vendas_hoje_labels": vendas_hoje_labels,
        "vendas_hoje_valores": vendas_hoje_valores,
        "crm": crm,
        "lancamento_form": lancamento_form,
        "lancamentos_recentes": lancamentos_recentes,
        "categorias_receita": categorias_receita,
        "categorias_despesa": categorias_despesa,
        "categorias_usuario": categorias_usuario,
        "categoria_usuario_atual": categoria_usuario_atual,
        "metas_usuarios": metas_usuarios,
        "metas_labels": metas_labels,
        "metas_valores": metas_valores,
        "metas_realizado_valores": metas_realizado_valores,
        "metas_fotos": metas_fotos,
        "meta_geral_total": meta_geral_total,
        "meta_geral_realizado": meta_geral_realizado,
        "meta_geral_progresso": meta_geral_progresso,
        "meta_geral_falta": meta_geral_falta,
    }
    return render(request, "financeiro/dashboard.html", contexto)


def _moeda(valor):
    return f"R$ {Decimal(str(valor or 0)):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def _resposta_pdf(buffer, nome):
    pdf = buffer.getvalue()
    buffer.close()
    response = HttpResponse(pdf, content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="{nome}"'
    return response


def _tabela(dados, larguras):
    tabela = Table(dados, colWidths=larguras, repeatRows=1)
    tabela.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#171a29")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
        ("ALIGN", (-1, 1), (-1, -1), "RIGHT"),
        ("BACKGROUND", (0, -1), (-1, -1), colors.HexColor("#eeeeee")),
        ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#cccccc")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
    ]))
    return tabela


def _grafico_barras(valores, labels, titulo):
    desenho = Drawing(720, 210)
    grafico = VerticalBarChart()
    grafico.x = 44
    grafico.y = 36
    grafico.height = 130
    grafico.width = 620
    grafico.data = [valores or [0]]
    grafico.categoryAxis.categoryNames = labels
    grafico.categoryAxis.labels.angle = 45
    grafico.categoryAxis.labels.fontSize = 7
    grafico.valueAxis.valueMin = 0
    grafico.valueAxis.valueMax = max(max(valores or [0]) * 1.2, 1)
    grafico.valueAxis.valueStep = max(round(grafico.valueAxis.valueMax / 4, 2), 1)
    grafico.bars[0].fillColor = colors.HexColor("#4b66ff")
    desenho.add(grafico)
    return [Paragraph(titulo, getSampleStyleSheet()["Heading3"]), desenho]


def relatorio_vendas_dia_pdf(vendas, dia, operador, escopo):
    total = vendas.aggregate(total=Sum("valor_total"))["total"] or Decimal("0.00")
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=landscape(A4),
        leftMargin=1.2 * cm,
        rightMargin=1.2 * cm,
        topMargin=1.1 * cm,
        bottomMargin=1.1 * cm,
    )
    styles = getSampleStyleSheet()
    elementos = [
        Paragraph("Relatorio Diario de Vendas", styles["Title"]),
        Paragraph(
            f"Dia: {dia.strftime('%d/%m/%Y')} | "
            f"Escopo: {'Geral' if escopo == 'geral' else operador.nome}",
            styles["Normal"],
        ),
        Spacer(1, 0.35 * cm),
    ]
    dados = [["Data", "Pedido", "Cliente", "Valor"]]
    for pedido in vendas[:500]:
        dados.append([
            pedido.data_pedido.strftime("%d/%m/%Y") if pedido.data_pedido else "-",
            f"#{pedido.legado_id or pedido.pk}",
            pedido.cliente.nome,
            _moeda(pedido.valor_total),
        ])
    dados.append(["", "", "Total", _moeda(total)])
    elementos.append(_tabela(dados, [2.5 * cm, 14 * cm, 7.2 * cm, 3 * cm]))
    doc.build(elementos)
    return _resposta_pdf(buffer, f"relatorio-vendas-dia-{dia:%Y%m%d}.pdf")


def relatorio_vendas_mes_pdf(pedidos, referencia, operador, escopo):
    inicio = referencia.replace(day=1)
    if inicio.month == 12:
        proximo_mes = inicio.replace(year=inicio.year + 1, month=1, day=1)
    else:
        proximo_mes = inicio.replace(month=inicio.month + 1, day=1)
    fim = proximo_mes - timedelta(days=1)
    vendas_mes = pedidos.filter(data_pedido__range=(inicio, fim)).order_by("data_pedido", "id")
    total_mes = vendas_mes.aggregate(total=Sum("valor_total"))["total"] or Decimal("0.00")
    vendas_por_dia = (
        vendas_mes.values("data_pedido").annotate(total=Sum("valor_total"), pedidos=Count("id")).order_by("data_pedido")
    )
    meses_comparacao = []
    labels = []
    valores = []
    cursor = inicio
    for offset in range(3, -1, -1):
        mes = cursor.month - offset
        ano = cursor.year
        while mes <= 0:
            mes += 12
            ano -= 1
        mes_inicio = cursor.replace(year=ano, month=mes, day=1)
        mes_fim = (mes_inicio.replace(year=ano + 1, month=1, day=1) if mes == 12 else mes_inicio.replace(month=mes + 1, day=1)) - timedelta(days=1)
        total = pedidos.filter(data_pedido__range=(mes_inicio, mes_fim)).aggregate(total=Sum("valor_total"))["total"] or Decimal("0.00")
        meses_comparacao.append((MESES_CURTOS[mes - 1], total))
        labels.append(MESES_CURTOS[mes - 1])
        valores.append(float(total))

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(A4), leftMargin=1.2 * cm, rightMargin=1.2 * cm, topMargin=1.1 * cm, bottomMargin=1.1 * cm)
    styles = getSampleStyleSheet()
    elementos = [
        Paragraph("Relatorio Mensal de Vendas", styles["Title"]),
        Paragraph(f"Mes: {MESES_CURTOS[inicio.month - 1]}/{inicio.year} | Escopo: {'Geral' if escopo == 'geral' else operador.nome}", styles["Normal"]),
        Spacer(1, 0.25 * cm),
        Paragraph(f"Total mensal: {_moeda(total_mes)} | Pedidos: {vendas_mes.count()} | Meta: nao configurada", styles["Heading3"]),
        Spacer(1, 0.2 * cm),
        *_grafico_barras(valores, labels, "Comparacao com meses anteriores"),
        Spacer(1, 0.25 * cm),
    ]
    dados_comparacao = [["Mes", "Total vendido"]] + [[mes, _moeda(total)] for mes, total in meses_comparacao]
    elementos.append(_tabela(dados_comparacao, [5 * cm, 5 * cm]))
    elementos.append(PageBreak())
    dados_dia = [["Dia", "Pedidos", "Total"]]
    for row in vendas_por_dia:
        dados_dia.append([row["data_pedido"].strftime("%d/%m/%Y"), row["pedidos"], _moeda(row["total"])])
    dados_dia.append(["Total", vendas_mes.count(), _moeda(total_mes)])
    elementos += [Paragraph("Vendas por dia", styles["Heading2"]), _tabela(dados_dia, [5 * cm, 4 * cm, 5 * cm])]
    doc.build(elementos)
    return _resposta_pdf(buffer, f"relatorio-vendas-mes-{inicio:%Y%m}.pdf")


def relatorio_crm_geral_pdf(crm, ano):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(A4), leftMargin=1.2 * cm, rightMargin=1.2 * cm, topMargin=1.1 * cm, bottomMargin=1.1 * cm)
    styles = getSampleStyleSheet()
    fluxo = crm["fluxo"]
    elementos = [
        Paragraph("Relatorio Geral do CRM", styles["Title"]),
        Paragraph(f"Ano: {ano}", styles["Normal"]),
        Spacer(1, 0.25 * cm),
        Paragraph(f"Receitas: {_moeda(fluxo['total_receitas'])} | Despesas: {_moeda(fluxo['total_despesas'])} | Lucro: {_moeda(fluxo['lucro'])} | Margem: {fluxo['margem']:.1f}%", styles["Heading3"]),
        Spacer(1, 0.2 * cm),
        *_grafico_barras([linha["receitas"] for linha in fluxo["linhas"]], crm["meses"], "Receitas por mes"),
        Spacer(1, 0.2 * cm),
        *_grafico_barras([linha["despesas"] for linha in fluxo["linhas"]], crm["meses"], "Despesas por mes"),
        PageBreak(),
    ]
    dados = [["Mes", "Receitas", "Despesas", "Lucro"]]
    for linha in fluxo["linhas"]:
        dados.append([linha["mes"], _moeda(linha["receitas"]), _moeda(linha["despesas"]), _moeda(linha["lucro"])])
    dados.append(["Total", _moeda(fluxo["total_receitas"]), _moeda(fluxo["total_despesas"]), _moeda(fluxo["lucro"])])
    elementos += [Paragraph("Fluxo de caixa anual", styles["Heading2"]), _tabela(dados, [5 * cm, 5 * cm, 5 * cm, 5 * cm])]
    doc.build(elementos)
    return _resposta_pdf(buffer, f"relatorio-crm-geral-{ano}.pdf")
