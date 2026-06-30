from decimal import Decimal

from django.contrib import messages
from django.db.models.deletion import ProtectedError
from django.db.models import Prefetch, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from apps.catalogo.assistencia import pedido_em_alerta, preparar_categorias_pedidos
from apps.catalogo.models import CategoriaServico, OperadorGestor, PerfilEmpresa, ProdutoServico
from apps.catalogo.os_config import css_linha_cabecalho, normalizar_campos_os
from apps.catalogo.permissions import operador_atual, pode_editar_pedido
from apps.clientes.models import Cliente, StatusCadastroCliente
from apps.financeiro.services import sincronizar_financeiro_pedido
from apps.pedidos.forms import PedidoCreateForm, PedidoEditForm, PedidoStatusForm
from apps.pedidos.models import (
    ArtePedido,
    PagamentoPedido,
    Pedido,
    PedidoItem,
    HistoricoStatusPedido,
    PrioridadePedido,
    STATUS_ENTREGA,
    STATUS_ASSISTENCIA,
    STATUS_FUNIL_GESTOR,
    STATUS_PRE_PRODUCAO,
    StatusPagamento,
    StatusPedido,
)


def pedido_list(request):
    operador = operador_atual(request)
    busca = request.GET.get("q", "").strip()
    status = request.GET.get("status", "").strip()
    categoria = request.GET.get("categoria", "").strip()
    modo_visualizacao = request.GET.get("visualizacao", "grade").strip()
    if modo_visualizacao not in {"grade", "lista"}:
        modo_visualizacao = "grade"
    itens_prefetch = Prefetch(
        "itens",
        queryset=PedidoItem.objects.select_related("produto__categoria_servico", "categoria_servico"),
    )
    pedidos = Pedido.objects.select_related("cliente").prefetch_related(itens_prefetch, "artes")

    if busca:
        filtros_busca = (
            Q(cliente__nome__icontains=busca)
            | Q(tema__icontains=busca)
            | Q(descricao_legada__icontains=busca)
            | Q(legado_id__icontains=busca)
            | Q(itens__nome__icontains=busca)
            | Q(itens__descricao__icontains=busca)
            | Q(itens__produto__nome__icontains=busca)
        )
        if busca.isdigit():
            filtros_busca |= Q(pk=int(busca)) | Q(legado_id=int(busca))
        pedidos = pedidos.filter(filtros_busca).distinct()
    if status == StatusPedido.EM_PRODUCAO:
        pedidos = pedidos.filter(status__in=STATUS_FUNIL_GESTOR)
    elif status:
        pedidos = pedidos.filter(status=status)
    if categoria:
        pedidos = pedidos.filter(
            Q(itens__categoria_servico_id=categoria) | Q(itens__produto__categoria_servico_id=categoria)
        ).distinct()

    pedidos_lista = preparar_categorias_pedidos(pedidos[:80])
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
        "em_producao": Pedido.objects.filter(status__in=STATUS_FUNIL_GESTOR).count(),
        "prontos": Pedido.objects.filter(status=StatusPedido.PRONTO).count(),
        "cancelados": Pedido.objects.filter(status=StatusPedido.CANCELADO).count(),
        "pode_acoes_admin": operador.is_admin,
    }
    return render(request, "pedidos/list.html", contexto)


def atendimento_list(request):
    operador = operador_atual(request)
    busca = request.GET.get("q", "").strip()
    pedidos = Pedido.objects.select_related("cliente").prefetch_related("itens", "artes").filter(status=StatusPedido.EM_ATENDIMENTO)
    if busca:
        filtros_busca = (
            Q(cliente__nome__icontains=busca)
            | Q(tema__icontains=busca)
            | Q(usuario_cadastro__icontains=busca)
            | Q(itens__nome__icontains=busca)
        )
        if busca.isdigit():
            filtros_busca |= Q(pk=int(busca)) | Q(legado_id=int(busca))
        pedidos = pedidos.filter(filtros_busca).distinct()
    return render(
        request,
        "pedidos/atendimento.html",
        {
            "active": "atendimento",
            "pedidos": pedidos.order_by("data_entrega", "id")[:120],
            "busca": busca,
            "total_atendimento": Pedido.objects.filter(status=StatusPedido.EM_ATENDIMENTO).count(),
            "meus_atendimento": Pedido.objects.filter(status=StatusPedido.EM_ATENDIMENTO, usuario_cadastro__iexact=operador.nome).count(),
        },
    )


def entrega_list(request):
    operador = operador_atual(request)
    itens_prefetch = Prefetch(
        "itens",
        queryset=PedidoItem.objects.select_related("produto__categoria_servico", "categoria_servico"),
    )
    pedidos = Pedido.objects.select_related("cliente").prefetch_related(itens_prefetch, "pagamentos", "artes").filter(
        status__in=STATUS_ENTREGA
    )
    pedidos_lista = preparar_categorias_pedidos(pedidos.order_by("data_entrega", "id")[:120])
    for pedido in pedidos_lista:
        pedido.alerta_prazo = pedido_em_alerta(pedido)
    contexto = {
        "active": "entrega",
        "pedidos": pedidos_lista,
        "prontos": pedidos.count(),
        "entregues": Pedido.objects.filter(status=StatusPedido.ENTREGUE).count(),
        "pode_acoes_admin": operador.is_admin,
    }
    return render(request, "pedidos/entrega.html", contexto)


def pedido_detail(request, pk):
    pedido = get_object_or_404(
        Pedido.objects.select_related("cliente").prefetch_related("itens", "artes", "pagamentos"),
        pk=pk,
    )
    operador = operador_atual(request)
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
    artes = list(pedido.artes.all().order_by("ordem", "id"))
    arte = artes[0] if artes else None
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
        "artes": artes,
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
    operador = operador_atual(request)
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
        "caminho_arquivo_corel": pedido.caminho_arquivo_corel,
        "valor_pago": pedido.valor_pago_legado,
        "forma_pagamento": pedido.forma_pagamento_legada,
        "desconto_ajuste": pedido.desconto_ajuste,
        "prioridade": pedido.prioridade,
        "canal_atendimento": pedido.canal_atendimento,
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
    operador = operador_atual(request)
    retorno = request.POST.get("next")
    if not (retorno and retorno.startswith("/") and not retorno.startswith("//")):
        retorno = None
    form = PedidoStatusForm(request.POST)
    if form.is_valid():
        novo_status = form.cleaned_data["status"]
        origem_producao = bool(retorno and retorno.startswith("/producao/"))
        if novo_status == StatusPedido.CANCELADO and not operador.pode_cancelar_pedido:
            messages.error(request, "Seu perfil não tem permissão para cancelar pedidos.")
            if retorno:
                return redirect(retorno)
            return redirect("pedido_detail", pk=pedido.pk)
        if not origem_producao and not pode_editar_pedido(pedido, operador) and novo_status != pedido.status:
            messages.error(request, "Seu perfil não tem permissão para alterar este pedido.")
            if retorno:
                return redirect(retorno)
            return redirect("pedido_detail", pk=pedido.pk)
        pedido.status = novo_status
        pedido.save(update_fields=["status", "atualizado_em"])
        sincronizar_financeiro_pedido(pedido)
        messages.success(request, "Status atualizado.")
    if retorno:
        return redirect(retorno)
    return redirect("pedido_detail", pk=pedido.pk)


def pedido_bulk_action(request):
    if request.method != "POST":
        return redirect("pedido_list")

    operador = operador_atual(request)
    retorno = request.POST.get("next")
    if not (retorno and retorno.startswith("/") and not retorno.startswith("//")):
        retorno = None
    acao = request.POST.get("acao", "").strip()
    ids = [valor for valor in request.POST.getlist("pedido_ids") if valor.isdigit()]
    pedidos = list(Pedido.objects.select_related("cliente").filter(pk__in=ids))

    if not pedidos:
        messages.warning(request, "Selecione pelo menos um pedido.")
        return redirect(retorno or "pedido_list")

    status_por_acao = {
        "marcar_pronto": StatusPedido.PRONTO,
        "enviar_producao": StatusPedido.EM_PRODUCAO,
        "marcar_entregue": StatusPedido.ENTREGUE,
        "cancelar": StatusPedido.CANCELADO,
    }

    if acao == "excluir":
        if not operador.is_admin:
            messages.error(request, "Somente administradores podem excluir pedidos.")
            return redirect(retorno or "pedido_list")
        excluidos = 0
        protegidos = 0
        for pedido in pedidos:
            arquivos_arte = [arte.arquivo for arte in pedido.artes.all()]
            try:
                pedido.delete()
                for arquivo in arquivos_arte:
                    arquivo.delete(save=False)
                excluidos += 1
            except ProtectedError:
                protegidos += 1
        if excluidos:
            messages.success(request, f"{excluidos} pedido(s) excluido(s).")
        if protegidos:
            messages.warning(request, f"{protegidos} pedido(s) possuem vinculos protegidos e nao foram excluidos.")
        return redirect(retorno or "pedido_list")

    novo_status = status_por_acao.get(acao)
    if not novo_status:
        messages.error(request, "Acao em massa invalida.")
        return redirect(retorno or "pedido_list")

    if novo_status == StatusPedido.CANCELADO and not operador.pode_cancelar_pedido:
        messages.error(request, "Somente administradores podem cancelar pedidos.")
        return redirect(retorno or "pedido_list")

    origem_operacional = bool(
        retorno
        and (
            retorno.startswith("/producao/")
            or retorno.startswith("/assistencia-envio/")
            or retorno.startswith("/pedidos/entrega/")
        )
    )
    atualizados = 0
    bloqueados = 0
    for pedido in pedidos:
        if (
            novo_status != StatusPedido.CANCELADO
            and not origem_operacional
            and not pode_editar_pedido(pedido, operador)
        ):
            bloqueados += 1
            continue
        if pedido.status == novo_status:
            continue
        pedido.status = novo_status
        pedido.save(update_fields=["status", "atualizado_em"])
        sincronizar_financeiro_pedido(pedido)
        atualizados += 1

    if atualizados:
        messages.success(request, f"{atualizados} pedido(s) atualizado(s).")
    if bloqueados:
        messages.warning(request, f"{bloqueados} pedido(s) ignorado(s) por permissao.")
    if not atualizados and not bloqueados:
        messages.info(request, "Nenhum pedido precisou ser alterado.")
    return redirect(retorno or "pedido_list")


def pedido_rejeitar_producao(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk)
    retorno = request.POST.get("next")
    if not (retorno and retorno.startswith("/") and not retorno.startswith("//")):
        retorno = "producao_home"
    motivo = (request.POST.get("motivo") or "").strip()
    if request.method != "POST":
        return redirect(retorno)
    if not motivo:
        messages.error(request, "Informe o motivo para devolver o pedido aos designers.")
        return redirect(retorno)
    if pedido.status != StatusPedido.EM_PRODUCAO:
        messages.error(request, "Somente pedidos em producao podem ser rejeitados.")
        return redirect(retorno)
    status_anterior = pedido.status
    pedido.status = StatusPedido.AGUARDANDO_ARTE
    pedido.save(update_fields=["status", "atualizado_em"])
    HistoricoStatusPedido.objects.create(
        pedido=pedido,
        status_anterior=status_anterior,
        status_novo=pedido.status,
        observacao=f"Rejeitado pela producao: {motivo}",
    )
    messages.warning(request, f"Pedido #{pedido.pk} devolvido para os designers.")
    return redirect(retorno)


def pedido_create(request):
    operador = operador_atual(request)
    hoje = timezone.localdate()
    cliente_prefill = Cliente.objects.filter(pk=request.GET.get("cliente")).first()
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
        initial = {
            "data_pedido": hoje,
            "data_entrega": hoje,
            "forma_pagamento": "PIX",
            "valor_pago": Decimal("0.00"),
            "desconto_ajuste": Decimal("0.00"),
            "prioridade": PrioridadePedido.NORMAL,
            "canal_atendimento": operador.canal_atendimento_padrao,
        }
        if cliente_prefill:
            initial.update(
                {
                    "nome_cliente": cliente_prefill.nome,
                    "telefone_1": cliente_prefill.telefone_principal,
                    "telefone_2": cliente_prefill.telefone_secundario,
                }
            )
        form = PedidoCreateForm(initial=initial)

    recentes = Pedido.objects.select_related("cliente").order_by("-id")[:6]
    prioridades = Pedido.objects.select_related("cliente").filter(
        status__in=STATUS_PRE_PRODUCAO
    ).order_by("data_entrega", "id")[:8]
    produtos = ProdutoServico.objects.select_related("categoria_servico").filter(ativo=True).order_by("nome")
    clientes_autocomplete = Cliente.objects.filter(
        status_cadastro=StatusCadastroCliente.CADASTRADO
    ).order_by("nome")[:400]
    return render(
        request,
        "pedidos/create.html",
        {
            "active": "novo_pedido",
            "form": form,
            "recentes": recentes,
            "prioridades": prioridades,
            "produtos": produtos,
            "clientes_autocomplete": clientes_autocomplete,
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
    if dados["marcar_pronto"]:
        status = StatusPedido.PRONTO
    elif dados["aguardar_arte"]:
        status = StatusPedido.AGUARDANDO_ARTE
    else:
        status = StatusPedido.ARTE_EM_PREPARO
    pedido = Pedido.objects.create(
        cliente=cliente,
        tema=dados["tema"].upper(),
        data_pedido=dados["data_pedido"],
        data_entrega=dados["data_entrega"],
        hora_entrega=dados.get("hora_entrega"),
        observacoes=dados.get("observacoes", ""),
        caminho_arquivo_corel=(dados.get("caminho_arquivo_corel") or "").strip(),
        valor_total=valor_total,
        valor_pago_legado=dados["valor_pago"],
        desconto_ajuste=dados["desconto_ajuste"],
        forma_pagamento_legada=dados["forma_pagamento"],
        prioridade=dados["prioridade"],
        canal_atendimento=dados["canal_atendimento"],
        status=status,
        origem="BALCAO",
        usuario_cadastro=(form.data.get("usuario_cadastro") or "").strip() or "Usuario Temporario",
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

    _sincronizar_pagamento_informado(pedido, dados["valor_pago"], dados["forma_pagamento"], dados["data_pedido"])

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


def _sincronizar_pagamento_informado(pedido, valor_pago, forma_pagamento, data_pagamento):
    valor_pago = valor_pago or Decimal("0.00")
    pagamentos = pedido.pagamentos.all()
    pagamento = pagamentos.filter(observacoes="Valor pago informado no pedido").first()
    if not pagamento and pagamentos.count() <= 1:
        pagamento = pagamentos.first()

    if valor_pago <= 0:
        if pagamento and pagamentos.count() <= 1:
            pagamento.delete()
        return

    dados = {
        "valor": valor_pago,
        "forma": forma_pagamento,
        "data_pagamento": data_pagamento,
        "status": StatusPagamento.CONFIRMADO,
        "observacoes": "Valor pago informado no pedido",
    }
    if pagamento:
        for campo, valor in dados.items():
            setattr(pagamento, campo, valor)
        pagamento.save(update_fields=list(dados.keys()))
    else:
        PagamentoPedido.objects.create(pedido=pedido, **dados)


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
    pedido.caminho_arquivo_corel = (dados.get("caminho_arquivo_corel") or "").strip()
    pedido.prioridade = dados["prioridade"]
    pedido.canal_atendimento = dados["canal_atendimento"]
    pedido.valor_total = subtotal + dados["desconto_ajuste"]
    pedido.valor_pago_legado = dados["valor_pago"]
    pedido.desconto_ajuste = dados["desconto_ajuste"]
    pedido.forma_pagamento_legada = dados["forma_pagamento"]
    pedido.status = dados["status"]
    pedido.usuario_cadastro = dados.get("usuario_cadastro", "").strip()
    pedido.save()
    _sincronizar_pagamento_informado(pedido, dados["valor_pago"], dados["forma_pagamento"], dados["data_pedido"])

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
