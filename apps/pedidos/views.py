from collections import defaultdict
from decimal import Decimal

from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from apps.catalogo.assistencia import categorias_do_pedido, pedido_em_alerta
from apps.catalogo.models import CategoriaServico, OperadorGestor, PerfilEmpresa, ProdutoServico
from apps.catalogo.os_config import css_linha_cabecalho, normalizar_campos_os
from apps.catalogo.permissions import operador_atual, pode_editar_pedido
from apps.clientes.models import Cliente
from apps.financeiro.services import sincronizar_financeiro_pedido
from apps.pedidos.forms import PedidoCreateForm, PedidoEditForm, PedidoStatusForm
from apps.pedidos.models import (
    ArtePedido,
    PagamentoPedido,
    Pedido,
    PedidoItem,
    PrioridadePedido,
    STATUS_ENTREGA,
    STATUS_PRE_PRODUCAO,
    STATUS_PRODUCAO,
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
        pedidos = pedidos.filter(
            Q(itens__categoria_servico_id=categoria) | Q(itens__produto__categoria_servico_id=categoria)
        ).distinct()

    pedidos_lista = list(pedidos[:80])
    for pedido in pedidos_lista:
        pedido.alerta_prazo = pedido_em_alerta(pedido)

    contexto = {
        "active": "pedidos",
        "pedidos": pedidos_lista,
        "busca": busca,
        "status_atual": status,
        "categoria_atual": categoria,
        "modo_visualizacao": modo_visualizacao,
        "categorias_tabs": CategoriaServico.objects.filter(ativa=True),
        "status_choices": StatusPedido.choices,
        "prioridade_choices": PrioridadePedido.choices,
        "total": Pedido.objects.count(),
        "pre_producao": Pedido.objects.filter(status__in=STATUS_PRE_PRODUCAO).count(),
        "em_producao": Pedido.objects.filter(status__in=STATUS_PRODUCAO).count(),
        "prontos": Pedido.objects.filter(status=StatusPedido.PRONTO).count(),
        "cancelados": Pedido.objects.filter(status=StatusPedido.CANCELADO).count(),
    }
    return render(request, "pedidos/list.html", contexto)


def producao_list(request):
    status = request.GET.get("status", "").strip()
    prioridade = request.GET.get("prioridade", "").strip()
    categoria = request.GET.get("categoria", "").strip()
    ordem = request.GET.get("ordem", "asc").strip()
    if ordem not in {"asc", "desc"}:
        ordem = "asc"
    pedidos = Pedido.objects.select_related("cliente").prefetch_related("itens", "artes").filter(
        status__in=STATUS_PRODUCAO
    )

    if status in STATUS_PRODUCAO:
        pedidos = pedidos.filter(status=status)
    if prioridade:
        pedidos = pedidos.filter(prioridade=prioridade)
    if categoria:
        pedidos = pedidos.filter(
            Q(itens__categoria_servico_id=categoria) | Q(itens__produto__categoria_servico_id=categoria)
        ).distinct()

    categorias = list(CategoriaServico.objects.filter(ativa=True).order_by("ordem", "nome"))
    pedidos_lista = list(pedidos.order_by("data_entrega" if ordem == "asc" else "-data_entrega", "id")[:180])
    grupos_map = defaultdict(list)
    sem_categoria = []
    for pedido in pedidos_lista:
        pedido.alerta_prazo = pedido_em_alerta(pedido)
        categorias_pedido = sorted(categorias_do_pedido(pedido), key=lambda item: (item.ordem, item.nome))
        if not categorias_pedido:
            sem_categoria.append(pedido)
            continue
        for categoria_pedido in categorias_pedido:
            grupos_map[categoria_pedido.id].append(pedido)

    grupos = [
        {"categoria": categoria_item, "pedidos": grupos_map.get(categoria_item.id, [])}
        for categoria_item in categorias
        if grupos_map.get(categoria_item.id)
    ]
    if sem_categoria:
        grupos.append({"categoria": None, "pedidos": sem_categoria})

    contexto = {
        "active": "producao",
        "grupos": grupos,
        "status_atual": status,
        "prioridade_atual": prioridade,
        "categoria_atual": categoria,
        "ordem": ordem,
        "ordem_inversa": "desc" if ordem == "asc" else "asc",
        "categorias_tabs": categorias,
        "prioridade_choices": PrioridadePedido.choices,
        "liberados": Pedido.objects.filter(status=StatusPedido.LIBERADO_PRODUCAO).count(),
        "produzindo": Pedido.objects.filter(status=StatusPedido.EM_PRODUCAO).count(),
        "urgentes": Pedido.objects.filter(status__in=STATUS_PRODUCAO, prioridade=PrioridadePedido.URGENTE).count(),
    }
    return render(request, "pedidos/producao.html", contexto)


def entrega_list(request):
    pedidos = Pedido.objects.select_related("cliente").prefetch_related("itens", "pagamentos").filter(
        status__in=STATUS_ENTREGA
    )
    pedidos_lista = list(pedidos.order_by("data_entrega", "id")[:120])
    for pedido in pedidos_lista:
        pedido.alerta_prazo = pedido_em_alerta(pedido)
    contexto = {
        "active": "entrega",
        "pedidos": pedidos_lista,
        "prontos": pedidos.count(),
        "entregues": Pedido.objects.filter(status=StatusPedido.ENTREGUE).count(),
    }
    return render(request, "pedidos/entrega.html", contexto)


def pedido_detail(request, pk):
    pedido = get_object_or_404(
        Pedido.objects.select_related("cliente").prefetch_related("itens", "artes", "pagamentos"),
        pk=pk,
    )
    operador = operador_atual()
    return render(
        request,
        "pedidos/detail.html",
        {
            "active": "pedidos",
            "pedido": pedido,
            "pode_editar": pode_editar_pedido(pedido, operador),
            "pode_cancelar": operador.pode_cancelar_pedido,
            "status_form": PedidoStatusForm(initial={"status": pedido.status}),
            "categorias_tabs": CategoriaServico.objects.filter(ativa=True),
        },
    )


def pedido_ordem_servico(request, pk):
    pedido = get_object_or_404(
        Pedido.objects.select_related("cliente").prefetch_related("itens", "artes", "pagamentos"),
        pk=pk,
    )
    perfil_empresa, _ = PerfilEmpresa.objects.get_or_create(chave="global")
    campos = normalizar_campos_os(perfil_empresa.os_campos)
    arte = pedido.artes.first()
    itens = list(pedido.itens.all())
    descricao = pedido.descricao_legada or " | ".join(str(item) for item in itens)
    designer_nome = (pedido.designer or pedido.usuario_cadastro or "").strip()
    designer_foto = None
    if designer_nome:
        operador_designer = OperadorGestor.objects.filter(nome__iexact=designer_nome).first()
        if operador_designer and operador_designer.foto:
            designer_foto = operador_designer.foto
    contexto = {
        "pedido": pedido,
        "perfil_empresa": perfil_empresa,
        "campos": campos,
        "arte": arte,
        "itens": itens,
        "descricao_os": descricao,
        "designer_foto": designer_foto,
        "os_header_line_css": css_linha_cabecalho(perfil_empresa.os_linha_cabecalho),
    }
    return render(request, "pedidos/ordem_servico.html", contexto)


def pedido_edit(request, pk):
    pedido = get_object_or_404(
        Pedido.objects.select_related("cliente").prefetch_related("itens", "artes"),
        pk=pk,
    )
    operador = operador_atual()
    if not pode_editar_pedido(pedido, operador):
        messages.error(request, "Seu perfil só permite editar pedidos cadastrados por você.")
        return redirect("pedido_detail", pk=pedido.pk)
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
        "prioridade": pedido.prioridade,
        "status": pedido.status,
        "usuario_cadastro": pedido.usuario_cadastro or "",
    }

    if request.method == "POST":
        acao = request.POST.get("acao")
        if acao == "remover_arte":
            if not operador.is_admin:
                messages.error(request, "Seu perfil não tem permissão para excluir informações do pedido.")
                return redirect("pedido_edit", pk=pedido.pk)
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
        messages.error(request, "Não foi possível salvar o pedido. Confira os campos destacados.")
    else:
        form = PedidoEditForm(initial=initial)

    produtos = ProdutoServico.objects.select_related("categoria_servico").filter(ativo=True).order_by("nome")
    itens = list(pedido.itens.all())
    itens_rows = (itens + [None] * 5)[:5]
    operadores = OperadorGestor.objects.filter(ativo=True).order_by("nome")
    return render(
        request,
        "pedidos/edit.html",
        {
            "active": "pedidos",
            "pedido": pedido,
            "form": form,
            "produtos": produtos,
            "operadores": operadores,
            "categorias_servico": CategoriaServico.objects.filter(ativa=True).order_by("ordem", "nome"),
            "itens_rows": itens_rows,
            "categorias_tabs": CategoriaServico.objects.filter(ativa=True),
        },
    )


def pedido_update_status(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk)
    operador = operador_atual()
    form = PedidoStatusForm(request.POST)
    if form.is_valid():
        novo_status = form.cleaned_data["status"]
        if novo_status == StatusPedido.CANCELADO and not operador.pode_cancelar_pedido:
            messages.error(request, "Seu perfil não tem permissão para cancelar pedidos.")
            return redirect("pedido_detail", pk=pedido.pk)
        if not pode_editar_pedido(pedido, operador) and novo_status != pedido.status:
            messages.error(request, "Seu perfil não tem permissão para alterar este pedido.")
            return redirect("pedido_detail", pk=pedido.pk)
        pedido.status = novo_status
        pedido.save(update_fields=["status", "atualizado_em"])
        sincronizar_financeiro_pedido(pedido)
        messages.success(request, "Status atualizado.")
    return redirect("pedido_detail", pk=pedido.pk)


def pedido_create(request):
    operador = operador_atual()
    hoje = timezone.localdate()
    if request.method == "POST":
        dados_post = request.POST.copy()
        dados_post["data_pedido"] = hoje.isoformat()
        form = PedidoCreateForm(dados_post, request.FILES)
        if form.is_valid():
            pedido = _criar_pedido(form, request.FILES.getlist("artes"))
            messages.success(request, f"Pedido #{pedido.pk} criado com sucesso.")
            return redirect("pedido_detail", pk=pedido.pk)
        messages.error(request, "Não foi possível criar o pedido. Confira os campos destacados.")
    else:
        form = PedidoCreateForm(
            initial={
                "data_pedido": hoje,
                "forma_pagamento": "PIX",
                "valor_pago": Decimal("0.00"),
                "desconto_ajuste": Decimal("0.00"),
                "prioridade": PrioridadePedido.NORMAL,
            }
        )

    recentes = Pedido.objects.select_related("cliente").order_by("-id")[:6]
    prioridades = Pedido.objects.select_related("cliente").filter(
        status__in=STATUS_PRE_PRODUCAO
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
            "categorias_servico": CategoriaServico.objects.filter(ativa=True).order_by("ordem", "nome"),
            "categorias_tabs": CategoriaServico.objects.filter(ativa=True),
            "operador_atual": operador,
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
        categoria = produto.categoria_servico if produto else CategoriaServico.objects.filter(pk=form.data.get(f"item_categoria_{index}") or None).first()
        quantidade = Decimal(form.data.get(f"item_qtd_{index}") or "1")
        preco = Decimal(str(form.data.get(f"item_preco_{index}") or "0").replace(",", "."))
        descricao = form.data.get(f"item_desc_{index}", "").strip()
        subtotal += quantidade * preco
        itens.append((index, nome, quantidade, preco, descricao, produto, categoria))

    valor_total = subtotal + dados["desconto_ajuste"]
    status = StatusPedido.PRONTO if dados["marcar_pronto"] else StatusPedido.AGUARDANDO_ARTE
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
        prioridade=dados["prioridade"],
        status=status,
        origem="BALCAO",
        usuario_cadastro=(form.data.get("usuario_cadastro") or "").strip(),
        data_registro=timezone.now(),
    )

    for ordem, nome, quantidade, preco, descricao, produto, categoria in itens:
        PedidoItem.objects.create(
            pedido=pedido,
            produto=produto,
            categoria_servico=categoria,
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
        categoria = produto.categoria_servico if produto else CategoriaServico.objects.filter(pk=form.data.get(f"item_categoria_{index}") or None).first()
        quantidade = Decimal(form.data.get(f"item_qtd_{index}") or "1")
        preco = Decimal(str(form.data.get(f"item_preco_{index}") or "0").replace(",", "."))
        descricao = form.data.get(f"item_desc_{index}", "").strip()
        subtotal += quantidade * preco
        PedidoItem.objects.create(
            pedido=pedido,
            produto=produto,
            categoria_servico=categoria,
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
    pedido.prioridade = dados["prioridade"]
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
