from decimal import Decimal

from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from apps.catalogo.models import CategoriaServico, ProdutoServico
from apps.clientes.models import Cliente
from apps.financeiro.services import sincronizar_financeiro_pedido
from apps.pedidos.forms import PedidoCreateForm, PedidoEditForm, PedidoStatusForm
from apps.pedidos.models import (
    ArtePedido,
    PagamentoPedido,
    Pedido,
    PedidoItem,
    StatusPagamento,
    StatusPedido,
)


def pedido_list(request):
    busca = request.GET.get("q", "").strip()
    status = request.GET.get("status", "").strip()
    categoria = request.GET.get("categoria", "").strip()
    modo_visualizacao = request.GET.get("visualizacao", "grade").strip()
    if modo_visualizacao not in {"grade", "lista"}:
        modo_visualizacao = "grade"
    pedidos = Pedido.objects.select_related("cliente").prefetch_related("itens", "artes")

    if busca:
        pedidos = pedidos.filter(
            Q(cliente__nome__icontains=busca)
            | Q(tema__icontains=busca)
            | Q(descricao_legada__icontains=busca)
            | Q(legado_id__icontains=busca)
        )
    if status:
        pedidos = pedidos.filter(status=status)
    if categoria:
        pedidos = pedidos.filter(itens__produto__categoria_servico_id=categoria).distinct()

    contexto = {
        "active": "pedidos",
        "pedidos": pedidos[:80],
        "busca": busca,
        "status_atual": status,
        "categoria_atual": categoria,
        "modo_visualizacao": modo_visualizacao,
        "categorias_tabs": CategoriaServico.objects.filter(ativa=True),
        "status_choices": StatusPedido.choices,
        "total": Pedido.objects.count(),
        "em_producao": Pedido.objects.filter(status__in=[StatusPedido.EM_PRODUCAO, StatusPedido.AGUARDANDO_ARTE]).count(),
        "prontos": Pedido.objects.filter(status=StatusPedido.PRONTO).count(),
        "cancelados": Pedido.objects.filter(status=StatusPedido.CANCELADO).count(),
    }
    return render(request, "pedidos/list.html", contexto)


def pedido_detail(request, pk):
    pedido = get_object_or_404(
        Pedido.objects.select_related("cliente").prefetch_related("itens", "artes", "pagamentos"),
        pk=pk,
    )
    return render(
        request,
        "pedidos/detail.html",
        {
            "active": "pedidos",
            "pedido": pedido,
            "status_form": PedidoStatusForm(initial={"status": pedido.status}),
            "categorias_tabs": CategoriaServico.objects.filter(ativa=True),
        },
    )


def pedido_edit(request, pk):
    pedido = get_object_or_404(
        Pedido.objects.select_related("cliente").prefetch_related("itens", "artes"),
        pk=pk,
    )
    cliente = pedido.cliente
    initial = {
        "nome_cliente": cliente.nome,
        "data_pedido": pedido.data_pedido,
        "tema": pedido.tema,
        "telefone_1": cliente.telefone_principal,
        "telefone_2": cliente.telefone_secundario,
        "data_entrega": pedido.data_entrega,
        "hora_entrega": pedido.hora_entrega,
        "observacoes": pedido.observacoes,
        "valor_pago": pedido.valor_pago_legado,
        "forma_pagamento": pedido.forma_pagamento_legada,
        "desconto_ajuste": pedido.desconto_ajuste,
        "status": pedido.status,
        "usuario_cadastro": pedido.usuario_cadastro or "",
    }

    if request.method == "POST":
        acao = request.POST.get("acao")
        if acao == "remover_arte":
            arte = get_object_or_404(ArtePedido, pk=request.POST.get("arte_id"), pedido=pedido)
            arte.arquivo.delete(save=False)
            arte.delete()
            messages.success(request, "Arte removida.")
            return redirect("pedido_edit", pk=pedido.pk)

        form = PedidoEditForm(request.POST, request.FILES)
        if form.is_valid():
            _atualizar_pedido(pedido, form, request.FILES.getlist("artes"))
            messages.success(request, "Pedido atualizado.")
            return redirect("pedido_detail", pk=pedido.pk)
    else:
        form = PedidoEditForm(initial=initial)

    produtos = ProdutoServico.objects.select_related("categoria_servico").filter(ativo=True).order_by("nome")
    itens = list(pedido.itens.all())
    itens_rows = (itens + [None] * 5)[:5]
    return render(
        request,
        "pedidos/edit.html",
        {
            "active": "pedidos",
            "pedido": pedido,
            "form": form,
            "produtos": produtos,
            "itens_rows": itens_rows,
            "categorias_tabs": CategoriaServico.objects.filter(ativa=True),
        },
    )


def pedido_update_status(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk)
    form = PedidoStatusForm(request.POST)
    if form.is_valid():
        pedido.status = form.cleaned_data["status"]
        pedido.save(update_fields=["status", "atualizado_em"])
        sincronizar_financeiro_pedido(pedido)
        messages.success(request, "Status atualizado.")
    return redirect("pedido_detail", pk=pedido.pk)


def pedido_create(request):
    if request.method == "POST":
        form = PedidoCreateForm(request.POST, request.FILES)
        if form.is_valid():
            pedido = _criar_pedido(form, request.FILES.getlist("artes"))
            messages.success(request, f"Pedido #{pedido.pk} criado com sucesso.")
            return redirect("pedido_detail", pk=pedido.pk)
    else:
        form = PedidoCreateForm(
            initial={
                "data_pedido": timezone.localdate(),
                "data_entrega": timezone.localdate(),
                "forma_pagamento": "PIX",
                "valor_pago": Decimal("0.00"),
                "desconto_ajuste": Decimal("0.00"),
            }
        )

    recentes = Pedido.objects.select_related("cliente").order_by("-id")[:6]
    prioridades = Pedido.objects.select_related("cliente").filter(
        status__in=[StatusPedido.EM_PRODUCAO, StatusPedido.AGUARDANDO_ARTE]
    ).order_by("data_entrega", "id")[:8]
    produtos = ProdutoServico.objects.select_related("categoria_servico").filter(ativo=True).order_by("nome")
    return render(
        request,
        "pedidos/create.html",
        {
            "active": "novo_pedido",
            "form": form,
            "recentes": recentes,
            "prioridades": prioridades,
            "produtos": produtos,
            "categorias_tabs": CategoriaServico.objects.filter(ativa=True),
        },
    )


def _criar_pedido(form, arquivos):
    dados = form.cleaned_data
    cliente, _ = Cliente.objects.get_or_create(
        nome=dados["nome_cliente"].upper(),
        defaults={
            "telefone_principal": dados.get("telefone_1", ""),
            "telefone_secundario": dados.get("telefone_2", ""),
        },
    )

    itens = []
    subtotal = Decimal("0.00")
    for index in range(1, 6):
        nome = form.data.get(f"item_nome_{index}", "").strip()
        if not nome:
            continue
        produto = ProdutoServico.objects.filter(nome__iexact=nome).first()
        quantidade = Decimal(form.data.get(f"item_qtd_{index}") or "1")
        preco = Decimal(str(form.data.get(f"item_preco_{index}") or "0").replace(",", "."))
        descricao = form.data.get(f"item_desc_{index}", "").strip()
        subtotal += quantidade * preco
        itens.append((index, nome, quantidade, preco, descricao, produto))

    valor_total = subtotal + dados["desconto_ajuste"]
    status = StatusPedido.PRONTO if dados["marcar_pronto"] else StatusPedido.EM_PRODUCAO
    pedido = Pedido.objects.create(
        cliente=cliente,
        tema=dados["tema"].upper(),
        data_pedido=dados["data_pedido"],
        data_entrega=dados["data_entrega"],
        hora_entrega=dados.get("hora_entrega"),
        observacoes=dados.get("observacoes", ""),
        valor_total=valor_total,
        valor_pago_legado=dados["valor_pago"],
        desconto_ajuste=dados["desconto_ajuste"],
        forma_pagamento_legada=dados["forma_pagamento"],
        status=status,
        origem="BALCAO",
        usuario_cadastro=(form.data.get("usuario_cadastro") or "").strip(),
        data_registro=timezone.now(),
    )

    for ordem, nome, quantidade, preco, descricao, produto in itens:
        PedidoItem.objects.create(
            pedido=pedido,
            produto=produto,
            ordem=ordem,
            nome=nome,
            quantidade=quantidade,
            preco_unitario=preco,
            custo_unitario_estimado=produto.custo_estimado if produto else Decimal("0.00"),
            descricao=descricao,
        )

    if dados["valor_pago"] > 0:
        PagamentoPedido.objects.create(
            pedido=pedido,
            valor=dados["valor_pago"],
            forma=dados["forma_pagamento"],
            data_pagamento=dados["data_pedido"],
            status=StatusPagamento.CONFIRMADO,
        )

    for ordem, arquivo in enumerate(arquivos):
        ArtePedido.objects.create(
            pedido=pedido,
            arquivo=arquivo,
            nome_original=arquivo.name,
            tamanho_bytes=arquivo.size,
            ordem=ordem,
        )

    sincronizar_financeiro_pedido(pedido)
    return pedido


def _atualizar_pedido(pedido, form, arquivos):
    dados = form.cleaned_data
    cliente = pedido.cliente
    cliente.nome = dados["nome_cliente"].upper()
    cliente.telefone_principal = dados.get("telefone_1", "")
    cliente.telefone_secundario = dados.get("telefone_2", "")
    cliente.save(update_fields=["nome", "telefone_principal", "telefone_secundario"])

    pedido.itens.all().delete()
    subtotal = Decimal("0.00")
    for index in range(1, 6):
        nome = form.data.get(f"item_nome_{index}", "").strip()
        if not nome:
            continue
        produto = ProdutoServico.objects.filter(nome__iexact=nome).first()
        quantidade = Decimal(form.data.get(f"item_qtd_{index}") or "1")
        preco = Decimal(str(form.data.get(f"item_preco_{index}") or "0").replace(",", "."))
        descricao = form.data.get(f"item_desc_{index}", "").strip()
        subtotal += quantidade * preco
        PedidoItem.objects.create(
            pedido=pedido,
            produto=produto,
            ordem=index,
            nome=nome,
            quantidade=quantidade,
            preco_unitario=preco,
            custo_unitario_estimado=produto.custo_estimado if produto else Decimal("0.00"),
            descricao=descricao,
        )

    pedido.tema = dados["tema"].upper()
    pedido.data_pedido = dados["data_pedido"]
    pedido.data_entrega = dados["data_entrega"]
    pedido.hora_entrega = dados.get("hora_entrega")
    pedido.observacoes = dados.get("observacoes", "")
    pedido.valor_total = subtotal + dados["desconto_ajuste"]
    pedido.valor_pago_legado = dados["valor_pago"]
    pedido.desconto_ajuste = dados["desconto_ajuste"]
    pedido.forma_pagamento_legada = dados["forma_pagamento"]
    pedido.status = dados["status"]
    pedido.usuario_cadastro = dados.get("usuario_cadastro", "").strip()
    pedido.save()

    ordem_base = pedido.artes.count()
    for offset, arquivo in enumerate(arquivos):
        ArtePedido.objects.create(
            pedido=pedido,
            arquivo=arquivo,
            nome_original=arquivo.name,
            tamanho_bytes=arquivo.size,
            ordem=ordem_base + offset,
        )

    sincronizar_financeiro_pedido(pedido)
    return pedido
