from django.contrib import messages
from django.core.exceptions import PermissionDenied, ValidationError
from django.shortcuts import get_object_or_404, redirect, render

from apps.catalogo.permissions import operador_atual
from .knowledge_services import aprovar_conhecimento, registrar_conhecimento
from .models import CamadaConhecimento, Conhecimento


def conhecimento_lista(request):
    operador = operador_atual(request)
    return render(request, "aprendizado/conhecimento.html", {
        "active": "aprendizado",
        "itens": Conhecimento.objects.all()[:100],
        "camadas": CamadaConhecimento.choices,
        "pode_aprovar": bool(operador and operador.is_admin),
    })


def conhecimento_registrar(request):
    if request.method != "POST":
        return redirect("conhecimento_lista")
    operador = operador_atual(request)
    try:
        registrar_conhecimento(
            operador=operador,
            titulo=request.POST.get("titulo"),
            conteudo=request.POST.get("conteudo"),
            camada=request.POST.get("camada"),
            fonte=request.POST.get("fonte"),
        )
        messages.success(request, "Conhecimento registrado para validação humana.")
    except (PermissionDenied, ValidationError) as exc:
        messages.error(request, str(exc))
    return redirect("conhecimento_lista")


def conhecimento_aprovar(request, conhecimento_id):
    if request.method != "POST":
        return redirect("conhecimento_lista")
    try:
        aprovar_conhecimento(conhecimento=get_object_or_404(Conhecimento, pk=conhecimento_id), operador=operador_atual(request))
        messages.success(request, "Conhecimento aprovado e versionado.")
    except (PermissionDenied, ValidationError) as exc:
        messages.error(request, str(exc))
    return redirect("conhecimento_lista")
