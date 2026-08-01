from django.contrib import messages
from django.shortcuts import redirect, render

from apps.auditoria.models import EventoOperacional
from apps.catalogo.permissions import operador_atual


def auditoria_lista(request):
    operador = operador_atual(request)
    if not operador or not operador.is_admin:
        messages.error(request, "Somente administradores podem consultar a auditoria.")
        return redirect("home")

    eventos = EventoOperacional.objects.select_related("operador")
    tipo = request.GET.get("tipo", "").strip()
    alvo = request.GET.get("alvo", "").strip()
    if tipo:
        eventos = eventos.filter(tipo=tipo)
    if alvo:
        eventos = eventos.filter(alvo_id=alvo)
    return render(
        request,
        "auditoria/lista.html",
        {"active": "auditoria", "eventos": eventos[:300], "tipo": tipo, "alvo": alvo},
    )
