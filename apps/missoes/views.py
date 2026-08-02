from django.contrib import messages
from django.core.exceptions import PermissionDenied, ValidationError
from django.db.models import Q
from django.http import Http404
from django.shortcuts import redirect, render
from apps.catalogo.permissions import operador_atual
from .forms import (
    BloquearMissaoForm,
    ConcluirMissaoForm,
    CriarMissaoIndividualForm,
    PausarMissaoForm,
    RetomarMissaoForm,
)
from .models import Missao
from .services import (
    bloquear_missao,
    concluir_missao,
    criar_missao_individual_voluntaria,
    iniciar_missao,
    pausar_missao,
    retomar_missao,
)


def _visiveis(operador):
    consulta = Missao.objects.select_related("criador", "responsavel_principal")
    return consulta if operador.is_admin else consulta.filter(Q(criador=operador) | Q(responsavel_principal=operador))


def lista_missoes(request):
    return render(request, "missoes/lista.html", {"active": "missoes", "missoes": _visiveis(operador_atual(request))[:200]})


def criar_missao(request):
    form = CriarMissaoIndividualForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        try:
            missao = criar_missao_individual_voluntaria(operador=operador_atual(request), **form.cleaned_data)
        except (PermissionDenied, ValidationError) as exc:
            form.add_error(None, str(exc))
        else:
            messages.success(request, "Missão planejada e preservada no workspace.")
            return redirect("missao_detalhe", missao_id=missao.pk)
    return render(request, "missoes/criar.html", {"active": "missoes", "form": form})


def detalhe_missao(request, missao_id):
    operador = operador_atual(request)
    missao = _visiveis(operador).filter(pk=missao_id).first()
    if not missao:
        raise Http404
    return render(request, "missoes/detalhe.html", {
        "active": "missoes",
        "missao": missao,
        "pode_alterar": missao.responsavel_principal_id == operador.pk,
        "pausar_form": PausarMissaoForm(),
        "retomar_form": RetomarMissaoForm(),
        "bloquear_form": BloquearMissaoForm(),
        "concluir_form": ConcluirMissaoForm(),
    })


def alterar_estado_missao(request, missao_id, acao):
    if request.method != "POST":
        raise Http404
    operador = operador_atual(request)
    missao = _visiveis(operador).filter(pk=missao_id).first()
    if not missao:
        raise Http404
    try:
        if acao == "iniciar":
            iniciar_missao(missao=missao, operador=operador)
        elif acao == "pausar":
            pausar_form = PausarMissaoForm(request.POST)
            if not pausar_form.is_valid():
                raise ValidationError("Revise os campos obrigatórios da pausa.")
            pausar_missao(missao=missao, operador=operador, **pausar_form.cleaned_data)
        elif acao == "retomar":
            retomar_form = RetomarMissaoForm(request.POST)
            if not retomar_form.is_valid():
                raise ValidationError("Revise os campos da retomada.")
            retomar_missao(missao=missao, operador=operador, **retomar_form.cleaned_data)
        elif acao == "bloquear":
            bloquear_form = BloquearMissaoForm(request.POST)
            if not bloquear_form.is_valid():
                raise ValidationError("Revise todos os campos obrigatórios do bloqueio.")
            bloquear_missao(missao=missao, operador=operador, **bloquear_form.cleaned_data)
        elif acao == "concluir":
            concluir_form = ConcluirMissaoForm(request.POST)
            if not concluir_form.is_valid():
                raise ValidationError("Informe o resultado alcançado.")
            concluir_missao(missao=missao, operador=operador, **concluir_form.cleaned_data)
        else:
            raise Http404
    except (PermissionDenied, ValidationError) as exc:
        messages.error(request, str(exc))
    else:
        messages.success(request, "Estado da missão atualizado com histórico preservado.")
    return redirect("missao_detalhe", missao_id=missao.pk)
