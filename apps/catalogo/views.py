import json

from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from apps.catalogo.assistencia import dias_uteis_restantes, pedidos_assistencia
from apps.catalogo.forms import CategoriaServicoForm, ProdutoServicoForm
from apps.catalogo.models import CategoriaServico, OperadorGestor, ProdutoServico
from apps.catalogo.ui_prefs import carregar_preferencias, garantir_operadores_padrao, salvar_preferencias
from apps.catalogo.widget_data import pedidos_para_widget, resumo_assistencia_envio
from apps.pedidos.models import Pedido, StatusPedido


def produtos(request):
    categoria_form = CategoriaServicoForm(prefix="categoria")
    produto_form = ProdutoServicoForm(prefix="produto")

    if request.method == "POST":
        acao = request.POST.get("acao")
        if acao == "categoria":
            categoria_form = CategoriaServicoForm(request.POST, prefix="categoria")
            if categoria_form.is_valid():
                categoria_form.save()
                messages.success(request, "Categoria criada.")
                return redirect("produtos")
        if acao == "produto":
            produto_form = ProdutoServicoForm(request.POST, prefix="produto")
            if produto_form.is_valid():
                produto_form.save()
                messages.success(request, "Produto criado.")
                return redirect("produtos")

    return render(
        request,
        "catalogo/produtos.html",
        {
            "active": "produtos",
            "categorias": CategoriaServico.objects.all(),
            "produtos": ProdutoServico.objects.select_related("categoria_servico").order_by("categoria_servico__ordem", "nome"),
            "categoria_form": categoria_form,
            "produto_form": produto_form,
        },
    )


def produto_editar(request, pk):
    produto = get_object_or_404(ProdutoServico, pk=pk)
    categoria_form = CategoriaServicoForm(prefix="categoria")
    produto_form = ProdutoServicoForm(request.POST or None, instance=produto, prefix="produto")

    if request.method == "POST" and produto_form.is_valid():
        produto_form.save()
        messages.success(request, "Produto atualizado.")
        return redirect("produtos")

    return render(
        request,
        "catalogo/produtos.html",
        {
            "active": "produtos",
            "categorias": CategoriaServico.objects.all(),
            "produtos": ProdutoServico.objects.select_related("categoria_servico").order_by("categoria_servico__ordem", "nome"),
            "categoria_form": categoria_form,
            "produto_form": produto_form,
            "produto_editando": produto,
        },
    )


def assistencia_envio(request):
    return render(
        request,
        "catalogo/assistencia_envio.html",
        {
            "active": "assistencia",
            "grupos": pedidos_assistencia(),
            "dias_uteis_restantes": dias_uteis_restantes,
        },
    )


def assistencia_marcar_enviado(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk)
    pedido.status = StatusPedido.PRONTO
    pedido.save(update_fields=["status", "atualizado_em"])
    messages.success(request, f"Pedido #{pedido.pk} marcado como pronto.")
    return redirect("assistencia_envio")


def configuracoes(request):
    garantir_operadores_padrao()
    if request.method == "POST":
        acao = request.POST.get("acao")
        if acao == "criar_operador":
            nome = request.POST.get("nome_operador", "").strip()
            if nome:
                OperadorGestor.objects.get_or_create(nome=nome, defaults={"ativo": True})
                messages.success(request, f"Usuário {nome} criado.")
            else:
                messages.error(request, "Informe o nome do novo usuário.")
            return redirect("configuracoes")

    db = settings.DATABASES["default"]
    legacy_db = settings.DATABASES.get("legacy", {})
    contexto = {
        "active": "configuracoes",
        "categorias": CategoriaServico.objects.filter(ativa=True).order_by("ordem", "nome"),
        "operadores": OperadorGestor.objects.filter(ativo=True),
        "preferencias": carregar_preferencias(),
        "db": db,
        "legacy_db": legacy_db,
        "zoom_opcoes": [85, 90, 95, 100, 110, 125, 150, 175],
        "intervalo_opcoes": [5, 10, 15, 30, 60],
        "visivel_opcoes": [30, 60, 120, 300],
    }
    return render(request, "catalogo/configuracoes.html", contexto)


def _categorias_da_requisicao(request):
    valor = request.GET.get("categorias", "")
    if not valor.strip():
        return None
    return [item.strip() for item in valor.split(",") if item.strip()]


def api_widget_prazos(request):
    pedidos = pedidos_para_widget(_categorias_da_requisicao(request))
    for pedido in pedidos:
        pedido["url"] = reverse("pedido_detail", args=[pedido["id"]])
    return JsonResponse({"pedidos": pedidos, "total": len(pedidos)})


def api_notificacao_assistencia(request):
    resumo = resumo_assistencia_envio(_categorias_da_requisicao(request))
    resumo["url"] = reverse("assistencia_envio")
    return JsonResponse(resumo)


@require_http_methods(["GET", "POST"])
def api_preferencias(request):
    if request.method == "GET":
        return JsonResponse(carregar_preferencias())
    try:
        payload = json.loads(request.body.decode("utf-8") or "{}")
    except json.JSONDecodeError:
        return JsonResponse({"erro": "JSON inválido"}, status=400)
    return JsonResponse(salvar_preferencias(payload))
