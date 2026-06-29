from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Count, Q, Sum
from django.shortcuts import get_object_or_404, redirect, render

from apps.clientes.forms import ClienteForm
from apps.clientes.models import Cliente
from apps.pedidos.models import Pedido


def clientes(request):
    busca = request.GET.get("q", "").strip()
    cliente_aberto = None
    pedidos_cliente = None
    cliente_id = request.GET.get("abrir") or request.GET.get("cliente_id")
    if cliente_id:
        cliente_aberto = get_object_or_404(Cliente, pk=cliente_id)
        pedidos_cliente = Paginator(
            cliente_aberto.pedidos.select_related("cliente").order_by("-data_pedido", "-id"),
            10,
        ).get_page(request.GET.get("pagina_pedidos") or 1)

    form = ClienteForm()
    if request.method == "POST":
        cliente_id = request.POST.get("cliente_id")
        instance = Cliente.objects.filter(pk=cliente_id).first() if cliente_id else None
        form = ClienteForm(request.POST, instance=instance)
        if form.is_valid():
            cliente = form.save(commit=False)
            cliente.nome = cliente.nome.strip().upper()
            cliente.save()
            messages.success(request, f"Cliente {cliente.nome} salvo.")
            proximo = request.POST.get("next") or ""
            if proximo.startswith("/") and not proximo.startswith("//"):
                return redirect(f"{proximo}?cliente={cliente.pk}")
            return redirect("clientes")
        messages.error(request, "Nao foi possivel salvar o cliente. Confira os campos.")

    clientes_qs = Cliente.objects.annotate(
        total_pedidos=Count("pedidos", distinct=True),
        total_vendido=Sum("pedidos__valor_total"),
    )
    if busca:
        clientes_qs = clientes_qs.filter(
            Q(nome__icontains=busca)
            | Q(telefone_principal__icontains=busca)
            | Q(telefone_secundario__icontains=busca)
            | Q(email__icontains=busca)
            | Q(cpf_cnpj__icontains=busca)
        )

    clientes_lista = clientes_qs.order_by("nome")[:120]
    total_clientes = Cliente.objects.count()
    clientes_com_pedido = Cliente.objects.filter(pedidos__isnull=False).distinct().count()
    pedidos_total = Pedido.objects.count()

    return render(
        request,
        "clientes/clientes.html",
        {
            "active": "clientes",
            "form": form,
            "clientes": clientes_lista,
            "cliente_aberto": cliente_aberto,
            "pedidos_cliente": pedidos_cliente,
            "busca": busca,
            "total_clientes": total_clientes,
            "clientes_com_pedido": clientes_com_pedido,
            "pedidos_total": pedidos_total,
            "next": request.GET.get("next", ""),
        },
    )


def cliente_excluir(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == "POST":
        if cliente.pedidos.exists():
            messages.warning(request, "Cliente possui pedidos vinculados e nao pode ser excluido.")
        else:
            nome = cliente.nome
            cliente.delete()
            messages.success(request, f"Cliente {nome} excluido.")
    return redirect("clientes")
