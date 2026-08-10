from django.contrib import messages
from django.core.exceptions import PermissionDenied, ValidationError
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from apps.catalogo.permissions import operador_atual
from .forms import (
    BloquearMissaoForm,
    ConcluirMissaoForm,
    ConvidarParticipanteForm,
    CriarMissaoColetivaForm,
    CriarMissaoIndividualForm,
    ManifestarConviteForm,
    PausarMissaoForm,
    RetomarMissaoForm,
    SairMissaoForm,
)
from .task_forms import TarefaMissaoForm, NotaMissaoForm, MensagemChatMissaoForm
from .models import Missao, ParticipacaoMissao, TipoMissao
from .services import (
    bloquear_missao,
    concluir_missao,
    convidar_participante,
    criar_missao_coletiva_espontanea,
    criar_missao_individual_voluntaria,
    iniciar_missao,
    manifestar_convite,
    pausar_missao,
    retomar_missao,
    responder_convite,
    sair_missao_espontanea,
    adicionar_tarefa_missao,
    concluir_tarefa_missao,
    adicionar_nota_missao,
    enviar_mensagem_chat_missao,
)


def _visiveis(operador):
    consulta = Missao.objects.select_related("criador", "responsavel_principal")
    return consulta if operador.is_admin else consulta.filter(
        Q(criador=operador)
        | Q(responsavel_principal=operador)
        | Q(participacoes__operador=operador, participacoes__encerrado_em__isnull=True)
    ).distinct()


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


def criar_missao_coletiva(request):
    operador = operador_atual(request)
    form = CriarMissaoColetivaForm(request.POST or None, operador=operador)
    if request.method == "POST" and form.is_valid():
        try:
            missao = criar_missao_coletiva_espontanea(
                operador=operador, **form.cleaned_data
            )
        except (PermissionDenied, ValidationError) as exc:
            form.add_error(None, str(exc))
        else:
            messages.success(request, "Missão coletiva criada e convites enviados.")
            return redirect("missao_detalhe", missao_id=missao.pk)
    return render(
        request,
        "missoes/criar_coletiva.html",
        {"active": "missoes", "form": form},
    )


def detalhe_missao(request, missao_id):
    operador = operador_atual(request)
    missao = _visiveis(operador).filter(pk=missao_id).first()
    if not missao:
        raise Http404
    participacao_atual = missao.participacoes.filter(
        operador=operador, encerrado_em__isnull=True
    ).first()
    return render(request, "missoes/detalhe_workspace.html", {
        "active": "missoes",
        "missao": missao,
        "pode_alterar": missao.responsavel_principal_id == operador.pk,
        "pausar_form": PausarMissaoForm(),
        "retomar_form": RetomarMissaoForm(),
        "bloquear_form": BloquearMissaoForm(),
        "concluir_form": ConcluirMissaoForm(),
        "participacao_atual": participacao_atual,
        "participacoes_atuais": missao.participacoes.filter(
            encerrado_em__isnull=True
        ).select_related("operador"),
        "participacoes_historicas": missao.participacoes.filter(
            encerrado_em__isnull=False
        ).select_related("operador"),
        "convidar_form": ConvidarParticipanteForm(missao=missao),
        "manifestar_form": ManifestarConviteForm(),
        "sair_form": SairMissaoForm(),
        "tarefa_form": TarefaMissaoForm(missao=missao),
        "nota_form": NotaMissaoForm(),
        "chat_form": MensagemChatMissaoForm(),
        "pode_convidar": (
            missao.tipo == TipoMissao.COLETIVA_ESPONTANEA
            and missao.responsavel_principal_id == operador.pk
        ),
    })


def convidar_na_missao(request, missao_id):
    if request.method != "POST":
        raise Http404
    operador = operador_atual(request)
    missao = _visiveis(operador).filter(pk=missao_id).first()
    if not missao:
        raise Http404
    form = ConvidarParticipanteForm(request.POST, missao=missao)
    if not form.is_valid():
        messages.error(request, "Selecione uma pessoa e um papel válidos.")
    else:
        try:
            convidar_participante(
                missao=missao,
                convidado=form.cleaned_data["operador"],
                operador=operador,
                papel=form.cleaned_data["papel"],
            )
        except (PermissionDenied, ValidationError) as exc:
            messages.error(request, str(exc))
        else:
            messages.success(request, "Convite registrado sem criar obrigação automática.")
    return redirect("missao_detalhe", missao_id=missao.pk)


def responder_convite_view(request, participacao_id, resposta):
    if request.method != "POST" or resposta not in {"aceitar", "recusar"}:
        raise Http404
    operador = operador_atual(request)
    participacao = get_object_or_404(
        ParticipacaoMissao, pk=participacao_id, operador=operador
    )
    try:
        responder_convite(
            participacao=participacao, operador=operador, aceitar=resposta == "aceitar"
        )
    except (PermissionDenied, ValidationError) as exc:
        messages.error(request, str(exc))
    else:
        messages.success(request, "Resposta ao convite preservada no histórico.")
    if resposta == "recusar":
        return redirect("missoes_lista")
    return redirect("missao_detalhe", missao_id=participacao.missao_id)


def manifestar_convite_view(request, participacao_id):
    if request.method != "POST":
        raise Http404
    operador = operador_atual(request)
    participacao = get_object_or_404(
        ParticipacaoMissao, pk=participacao_id, operador=operador
    )
    form = ManifestarConviteForm(request.POST)
    if not form.is_valid():
        messages.error(request, "Informe o tipo e a mensagem.")
    else:
        try:
            manifestar_convite(
                participacao=participacao,
                operador=operador,
                **form.cleaned_data,
            )
        except (PermissionDenied, ValidationError) as exc:
            messages.error(request, str(exc))
        else:
            messages.success(request, "Manifestação enviada sem aceitar a participação.")
    return redirect("missao_detalhe", missao_id=participacao.missao_id)


def sair_missao_view(request, participacao_id):
    if request.method != "POST":
        raise Http404
    operador = operador_atual(request)
    participacao = get_object_or_404(
        ParticipacaoMissao, pk=participacao_id, operador=operador
    )
    form = SairMissaoForm(request.POST)
    if not form.is_valid():
        messages.error(request, "Confirme a saída e registre o motivo.")
    else:
        try:
            sair_missao_espontanea(
                participacao=participacao,
                operador=operador,
                **form.cleaned_data,
            )
        except (PermissionDenied, ValidationError) as exc:
            messages.error(request, str(exc))
        else:
            messages.success(request, "Saída registrada sem apagar suas contribuições.")
    return redirect("missoes_lista")


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


def adicionar_tarefa_view(request, missao_id):
    if request.method != "POST":
        raise Http404
    operador = operador_atual(request)
    missao = _visiveis(operador).filter(pk=missao_id).first()
    if not missao:
        raise Http404
    form = TarefaMissaoForm(request.POST, missao=missao)
    try:
        if not form.is_valid():
            raise ValidationError("Revise os campos da tarefa.")
        adicionar_tarefa_missao(missao=missao, operador=operador, **form.cleaned_data)
        messages.success(request, "Tarefa adicionada à missão.")
    except (PermissionDenied, ValidationError) as exc:
        messages.error(request, str(exc))
    return redirect("missao_detalhe", missao_id=missao.pk)


def concluir_tarefa_view(request, tarefa_id):
    if request.method != "POST":
        raise Http404
    operador = operador_atual(request)
    from .models import TarefaMissao
    tarefa = get_object_or_404(TarefaMissao, pk=tarefa_id)
    if not _visiveis(operador).filter(pk=tarefa.missao_id).exists():
        raise Http404
    try:
        concluir_tarefa_missao(tarefa=tarefa, operador=operador)
        messages.success(request, "Tarefa concluída.")
    except (PermissionDenied, ValidationError) as exc:
        messages.error(request, str(exc))
    return redirect("missao_detalhe", missao_id=tarefa.missao_id)


def adicionar_nota_view(request, missao_id):
    if request.method != "POST":
        raise Http404
    operador = operador_atual(request)
    missao = _visiveis(operador).filter(pk=missao_id).first()
    if not missao:
        raise Http404
    form = NotaMissaoForm(request.POST)
    try:
        if not form.is_valid():
            raise ValidationError("Revise os campos da nota.")
        adicionar_nota_missao(missao=missao, operador=operador, **form.cleaned_data)
        messages.success(request, "Nota registrada na missão.")
    except (PermissionDenied, ValidationError) as exc:
        messages.error(request, str(exc))
    return redirect("missao_detalhe", missao_id=missao.pk)


def enviar_chat_view(request, missao_id):
    if request.method != "POST":
        raise Http404
    operador = operador_atual(request)
    missao = _visiveis(operador).filter(pk=missao_id).first()
    if not missao:
        raise Http404
    form = MensagemChatMissaoForm(request.POST)
    try:
        if not form.is_valid():
            raise ValidationError("Digite uma mensagem.")
        enviar_mensagem_chat_missao(missao=missao, operador=operador, **form.cleaned_data)
        messages.success(request, "Mensagem enviada.")
    except (PermissionDenied, ValidationError) as exc:
        messages.error(request, str(exc))
    return redirect("missao_detalhe", missao_id=missao.pk)
