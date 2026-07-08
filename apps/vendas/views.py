from decimal import Decimal
from datetime import timedelta
from io import BytesIO

from django.contrib import messages
from django.db.models import Count, DecimalField, ExpressionWrapper, F, Sum
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils import timezone
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from apps.catalogo.forms import OperadorPerfilForm, OperadorSenhaForm, senha_operador_valida
from apps.catalogo.models import CategoriaServico, ProdutoServico
from apps.catalogo.permissions import operador_atual
from apps.catalogo.ui_prefs import salvar_preferencias
from apps.clientes.models import Cliente, StatusCadastroCliente
from apps.financeiro.crm import MESES_CURTOS
from apps.financeiro.models import LancamentoFinanceiro, MetaVendasUsuario, StatusLancamento, TipoLancamento
from apps.pedidos.models import Pedido, PedidoItem, StatusPedido
from apps.vendas.forms import VendasPedidoForm
from apps.vendas.services import criar_pedido_vendas


def _contexto_base(request):
    operador = operador_atual(request)
    return {
        "modo_vendas": True,
        "operador_atual": operador,
    }


def vendas_pedidos(request):
    operador = operador_atual(request)
    pedidos = (
        Pedido.objects.select_related("cliente")
        .filter(origem="VENDAS")
        .order_by("-criado_em")[:30]
    )
    contexto = _contexto_base(request)
    contexto.update(
        {
            "pedidos": pedidos,
            "active": "home",
            "pendentes": Pedido.objects.filter(origem="VENDAS", status=StatusPedido.EM_ATENDIMENTO).count(),
            "hoje": Pedido.objects.filter(origem="VENDAS", data_pedido=timezone.localdate()).count(),
            "meus": Pedido.objects.filter(origem="VENDAS", usuario_cadastro__iexact=operador.nome).count(),
        }
    )
    return render(request, "vendas/home.html", contexto)


def _pedidos_usuario(operador):
    return Pedido.objects.select_related("cliente").exclude(status=StatusPedido.CANCELADO).filter(usuario_cadastro__iexact=operador.nome)


def vendas_dashboard(request):
    operador = operador_atual(request)
    hoje = timezone.localdate()
    inicio_mes = hoje.replace(day=1)
    ano = hoje.year
    pedidos = _pedidos_usuario(operador)
    vendas_hoje = pedidos.filter(data_pedido=hoje)
    vendas_mes = pedidos.filter(data_pedido__range=(inicio_mes, hoje))
    meta_usuario, _ = MetaVendasUsuario.objects.get_or_create(
        operador=operador,
        ano=inicio_mes.year,
        mes=inicio_mes.month,
        defaults={"valor": Decimal("0.00")},
    )
    total_mes = vendas_mes.aggregate(total=Sum("valor_total"))["total"] or Decimal("0.00")
    total_hoje = vendas_hoje.aggregate(total=Sum("valor_total"))["total"] or Decimal("0.00")
    progresso = (total_mes / meta_usuario.valor * 100) if meta_usuario.valor else Decimal("0.00")
    falta_meta = max(Decimal("0.00"), meta_usuario.valor - total_mes)

    mes_anterior_fim = inicio_mes - timedelta(days=1)
    mes_anterior_inicio = mes_anterior_fim.replace(day=1)
    vendas_mes_anterior_total = (
        pedidos.filter(data_pedido__range=(mes_anterior_inicio, mes_anterior_fim)).aggregate(total=Sum("valor_total"))["total"]
        or Decimal("0.00")
    )
    crescimento_mes = (
        ((total_mes - vendas_mes_anterior_total) / vendas_mes_anterior_total) * 100
        if vendas_mes_anterior_total
        else Decimal("0.00")
    )

    meses = MESES_CURTOS
    receita_mensal = [0.0] * 12
    for row in (
        pedidos.filter(data_pedido__year=ano)
        .values("data_pedido__month")
        .annotate(total=Sum("valor_total"))
    ):
        mes = row["data_pedido__month"]
        if mes:
            receita_mensal[mes - 1] = float(row["total"] or 0)

    despesa_mensal = [0.0] * 12
    if operador.is_admin_geral:
        for row in (
            LancamentoFinanceiro.objects.exclude(status=StatusLancamento.CANCELADO)
            .filter(data_competencia__year=ano, tipo=TipoLancamento.DESPESA)
            .values("data_competencia__month")
            .annotate(total=Sum("valor"))
        ):
            mes = row["data_competencia__month"]
            if mes:
                despesa_mensal[mes - 1] = float(row["total"] or 0)

    vendas_hoje_labels = [f"{hora:02d}h" for hora in range(8, 19)]
    vendas_hoje_valores = [
        float(vendas_hoje.filter(criado_em__hour=hora).aggregate(total=Sum("valor_total"))["total"] or 0)
        for hora in range(8, 19)
    ]

    pedidos_ids = pedidos.values("id")
    top_produtos = list(
        PedidoItem.objects.filter(pedido_id__in=pedidos_ids)
        .values("nome")
        .annotate(quantidade=Sum("quantidade"))
        .order_by("-quantidade")[:6]
    )

    contexto = _contexto_base(request)
    contexto.update(
        {
            "active": "dashboard",
            "meta_usuario": meta_usuario,
            "total_mes": total_mes,
            "total_hoje": total_hoje,
            "pedidos_mes": vendas_mes.count(),
            "pedidos_hoje": vendas_hoje.count(),
            "ticket_medio": total_mes / vendas_mes.count() if vendas_mes.count() else Decimal("0.00"),
            "progresso": progresso,
            "falta_meta": falta_meta,
            "vendas_mes_anterior_total": vendas_mes_anterior_total,
            "crescimento_mes": crescimento_mes,
            "meses": meses,
            "receita_mensal": receita_mensal,
            "despesa_mensal": despesa_mensal,
            "vendas_hoje_labels": vendas_hoje_labels,
            "vendas_hoje_valores": vendas_hoje_valores,
            "produtos_labels": [row["nome"] for row in top_produtos],
            "produtos_valores": [float(row["quantidade"] or 0) for row in top_produtos],
            "pode_ver_fluxo_caixa": operador.is_admin_geral,
            "pedidos_recentes": pedidos.order_by("-data_pedido", "-id")[:8],
        }
    )
    return render(request, "vendas/dashboard.html", contexto)


def _moeda(valor):
    return f"R$ {Decimal(str(valor or 0)):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def _tabela(dados, larguras):
    tabela = Table(dados, colWidths=larguras, repeatRows=1)
    tabela.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#171a29")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#cccccc")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
    ]))
    return tabela


def vendas_relatorio(request, tipo):
    operador = operador_atual(request)
    hoje = timezone.localdate()
    pedidos = _pedidos_usuario(operador)
    if tipo == "diario":
        inicio = fim = hoje
        titulo = "Relatorio Diario - Mheibos Vendas"
        nome = f"mheibos-vendas-diario-{hoje:%Y%m%d}.pdf"
    else:
        inicio = hoje.replace(day=1)
        fim = hoje
        titulo = "Relatorio Mensal - Mheibos Vendas"
        nome = f"mheibos-vendas-mensal-{hoje:%Y%m}.pdf"
    vendas = pedidos.filter(data_pedido__range=(inicio, fim)).order_by("data_pedido", "id")
    total = vendas.aggregate(total=Sum("valor_total"))["total"] or Decimal("0.00")
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(A4), leftMargin=1.2 * cm, rightMargin=1.2 * cm, topMargin=1.1 * cm, bottomMargin=1.1 * cm)
    styles = getSampleStyleSheet()
    elementos = [
        Paragraph(titulo, styles["Title"]),
        Paragraph(f"Vendedora: {operador.nome} | Periodo: {inicio:%d/%m/%Y} a {fim:%d/%m/%Y}", styles["Normal"]),
        Spacer(1, 0.3 * cm),
        Paragraph(f"Total: {_moeda(total)} | Pedidos: {vendas.count()}", styles["Heading3"]),
        Spacer(1, 0.25 * cm),
    ]
    dados = [["Data", "Pedido", "Cliente", "Resumo", "Status", "Valor"]]
    for pedido in vendas[:500]:
        dados.append([
            pedido.data_pedido.strftime("%d/%m/%Y") if pedido.data_pedido else "-",
            f"#{pedido.legado_id or pedido.pk}",
            pedido.cliente.nome,
            pedido.tema or "-",
            pedido.get_status_display(),
            _moeda(pedido.valor_total),
        ])
    dados.append(["", "", "", "", "Total", _moeda(total)])
    elementos.append(_tabela(dados, [2.3 * cm, 2.2 * cm, 6 * cm, 8 * cm, 4 * cm, 3 * cm]))
    doc.build(elementos)
    pdf = buffer.getvalue()
    buffer.close()
    response = HttpResponse(pdf, content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="{nome}"'
    return response


def vendas_configuracoes(request):
    operador = operador_atual(request)
    perfil_form = OperadorPerfilForm(prefix="perfil", instance=operador)
    senha_form = OperadorSenhaForm(prefix="senha")
    if request.method == "POST":
        acao = request.POST.get("acao")
        if acao == "salvar_perfil":
            nome_anterior = operador.nome
            perfil_form = OperadorPerfilForm(request.POST, request.FILES, prefix="perfil", instance=operador)
            senha_atual = (request.POST.get("senha_atual") or "").strip()
            if not senha_operador_valida(operador, senha_atual):
                messages.error(request, "Senha incorreta. Informe sua senha atual para salvar o perfil.")
            elif perfil_form.is_valid():
                perfil_form.save()
                if operador.nome != nome_anterior:
                    salvar_preferencias({"usuario": operador.nome}, request=request)
                    request.session["operador_nome"] = operador.nome
                messages.success(request, "Perfil salvo.")
                return redirect("vendas_configuracoes")
            else:
                messages.error(request, "Nao foi possivel salvar seu perfil. Confira os campos.")
        elif acao == "trocar_senha":
            senha_form = OperadorSenhaForm(request.POST, prefix="senha")
            if senha_form.is_valid():
                dados = senha_form.cleaned_data
                if not senha_operador_valida(operador, dados["senha_atual"]):
                    senha_form.add_error("senha_atual", "Senha atual incorreta.")
                else:
                    operador.senha = dados["senha_nova"]
                    operador.save(update_fields=["senha", "atualizado_em"])
                    messages.success(request, "Senha alterada com sucesso.")
                    return redirect("vendas_configuracoes")
            messages.error(request, "Nao foi possivel alterar a senha. Confira os campos.")

    contexto = _contexto_base(request)
    contexto.update(
        {
            "active": "configuracoes",
            "perfil_form": perfil_form,
            "senha_form": senha_form,
        }
    )
    return render(request, "vendas/configuracoes.html", contexto)


def vendas_pedido_novo(request):
    operador = operador_atual(request)
    if request.method == "POST":
        form = VendasPedidoForm(request.POST)
        if form.is_valid():
            pedido = criar_pedido_vendas(form, operador.nome)
            messages.success(request, f"Pedido #{pedido.pk} enviado para Atendimento.")
            return redirect("vendas_home")
        messages.error(request, "Nao foi possivel salvar. Confira os campos.")
    else:
        form = VendasPedidoForm(initial={
            "forma_pagamento": "PIX",
            "valor_pago": 0,
            "desconto_ajuste": 0,
            "canal_atendimento": operador.canal_atendimento_padrao,
        })

    contexto = _contexto_base(request)
    contexto.update(
        {
            "form": form,
            "active": "novo",
            "clientes_autocomplete": Cliente.objects.filter(
                status_cadastro=StatusCadastroCliente.CADASTRADO
            ).order_by("nome")[:400],
            "produtos": ProdutoServico.objects.select_related("categoria_servico").filter(ativo=True).order_by("nome"),
            "categorias_servico": CategoriaServico.objects.filter(ativa=True).order_by("ordem", "nome"),
        }
    )
    return render(request, "vendas/novo_pedido.html", contexto)
