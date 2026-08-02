from django.contrib import messages
from django.core.exceptions import PermissionDenied, ValidationError
from django.db.models import Q
from django.http import Http404
from django.shortcuts import redirect, render
from apps.catalogo.permissions import operador_atual
from .forms import CriarMissaoIndividualForm
from .models import Missao
from .services import criar_missao_individual_voluntaria


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
    missao = _visiveis(operador_atual(request)).filter(pk=missao_id).first()
    if not missao:
        raise Http404
    return render(request, "missoes/detalhe.html", {"active": "missoes", "missao": missao})
