from django.shortcuts import render

from apps.catalogo.permissions import operador_atual

from .models import UnidadeSincronizacao


def painel(request):
    operador = operador_atual(request)
    unidades = UnidadeSincronizacao.objects.select_related("pedido_local", "operador")
    if not operador.is_admin:
        unidades = unidades.filter(operador=operador)
    return render(request, "sincronizacao/painel.html", {"active": "sincronizacao", "unidades": unidades[:100]})
