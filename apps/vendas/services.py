from decimal import Decimal

from django.utils import timezone

from apps.catalogo.models import CategoriaServico, ProdutoServico
from apps.clientes.models import Cliente
from apps.financeiro.services import sincronizar_financeiro_pedido
from apps.pedidos.models import (
    PagamentoPedido,
    Pedido,
    PedidoItem,
    OrigemPedido,
    StatusPagamento,
    StatusPedido,
)


def _decimal(valor, padrao="0"):
    return Decimal(str(valor or padrao).replace(",", "."))


def criar_pedido_vendas(form, vendedor_nome):
    dados = form.cleaned_data
    cliente, criado = Cliente.objects.get_or_create(
        nome=dados["nome_cliente"].strip().upper(),
        defaults={
            "telefone_principal": dados.get("telefone_1", ""),
            "telefone_secundario": dados.get("telefone_2", ""),
            "cpf_cnpj": dados.get("cpf_cnpj", ""),
            "endereco": dados.get("endereco", ""),
        },
    )
    if not criado:
        campos_atualizar = []
        for campo, valor in {
            "telefone_principal": dados.get("telefone_1", ""),
            "telefone_secundario": dados.get("telefone_2", ""),
            "cpf_cnpj": dados.get("cpf_cnpj", ""),
            "endereco": dados.get("endereco", ""),
        }.items():
            if valor and not getattr(cliente, campo):
                setattr(cliente, campo, valor)
                campos_atualizar.append(campo)
        if campos_atualizar:
            campos_atualizar.append("atualizado_em")
            cliente.save(update_fields=campos_atualizar)

    itens = []
    subtotal = Decimal("0.00")
    for index in range(1, 6):
        nome = form.data.get(f"item_nome_{index}", "").strip()
        if not nome:
            continue
        produto = ProdutoServico.objects.filter(nome__iexact=nome).select_related("categoria_servico").first()
        categoria = produto.categoria_servico if produto else CategoriaServico.objects.filter(pk=form.data.get(f"item_categoria_{index}") or None).first()
        quantidade = _decimal(form.data.get(f"item_qtd_{index}"), "1")
        preco = _decimal(form.data.get(f"item_preco_{index}"))
        descricao = form.data.get(f"item_desc_{index}", "").strip()
        subtotal += quantidade * preco
        itens.append((index, nome, quantidade, preco, descricao, produto, categoria))

    pedido = Pedido.objects.create(
        cliente=cliente,
        tema=dados["tema"].strip().upper(),
        data_pedido=timezone.localdate(),
        data_entrega=dados["data_entrega"],
        hora_entrega=dados.get("hora_entrega"),
        observacoes=dados.get("observacoes", ""),
        valor_total=subtotal + dados["desconto_ajuste"],
        valor_pago_legado=dados["valor_pago"],
        desconto_ajuste=dados["desconto_ajuste"],
        forma_pagamento_legada=dados["forma_pagamento"],
        prioridade=dados["prioridade"],
        status=StatusPedido.EM_ATENDIMENTO,
        origem=OrigemPedido.VENDAS,
        usuario_cadastro=vendedor_nome,
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
            data_pagamento=pedido.data_pedido,
            status=StatusPagamento.CONFIRMADO,
            observacoes="Valor pago informado no Mheibos Vendas",
        )

    sincronizar_financeiro_pedido(pedido)
    return pedido
