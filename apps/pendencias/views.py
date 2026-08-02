from django.db.models import Q
from django.shortcuts import render

from apps.catalogo.permissions import operador_atual

from .models import EstadoPendencia, Pendencia


def lista_pendencias(request):
    operador = operador_atual(request)
    pendencias = Pendencia.objects.select_related(
        "pedido__cliente", "processo", "responsavel_principal"
    ).prefetch_related("destinatarios")
    if not operador.is_admin:
        pendencias = pendencias.filter(
            Q(responsavel_principal=operador) | Q(destinatarios=operador)
        ).distinct()
    estado = request.GET.get("estado", EstadoPendencia.ABERTA)
    if estado in EstadoPendencia.values:
        pendencias = pendencias.filter(estado=estado)
    return render(
        request,
        "pendencias/lista.html",
        {"active": "pendencias", "pendencias": pendencias[:200], "estado": estado},
    )
