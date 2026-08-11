import json
from datetime import datetime

from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from apps.catalogo.permissions import operador_atual
from apps.missoes.models import EstadoMissao, EstadoTarefaMissao, Missao, TarefaMissao
from apps.pendencias.models import EstadoPendencia, Pendencia

from .models import Analise, EvidenciaAnalitica, Simulacao, TipoEvidencia
from .services import criar_analise_deterministica, gerar_relatorio_operacional, obter_metricas_operacionais, promover_simulacao_para_missao, registrar_evidencia, salvar_simulacao, validar_analise


def _operador_missoes(operador):
    return Q(criador=operador) | Q(responsavel_principal=operador) | Q(participacoes__operador=operador, participacoes__estado_participacao="ACEITO")


def dashboard(request):
    if request.GET.get("aba") in {"relatorios", "crm", "metas"}:
        query = request.GET.urlencode()
        return redirect(f"/financeiro/dashboard/?{query}")
    operador = operador_atual(request)
    missoes = Missao.objects.filter(_operador_missoes(operador)).exclude(estado__in={EstadoMissao.CONCLUIDA, EstadoMissao.CANCELADA, EstadoMissao.ARQUIVADA}).distinct()
    tarefas = TarefaMissao.objects.filter(missao__in=missoes, estado__in={EstadoTarefaMissao.PENDENTE, EstadoTarefaMissao.EM_ANDAMENTO}).select_related("missao")[:8]
    pendencias = Pendencia.objects.filter(Q(responsavel_principal=operador) | Q(destinatarios=operador), estado=EstadoPendencia.ABERTA).select_related("pedido")[:8]
    simulacoes = Simulacao.objects.filter(autor=operador).select_related("missao")[:5]
    return render(request, "analytics/dashboard.html", {"operador_atual": operador, "missoes": missoes[:8], "tarefas": tarefas, "pendencias": pendencias, "simulacoes": simulacoes, "metricas": obter_metricas_operacionais(operador=operador), "active": "dashboard"})


def analytics_home(request):
    operador = operador_atual(request)
    hoje = timezone.localdate()
    relatorio = gerar_relatorio_operacional(operador=operador, inicio=hoje.replace(day=1), fim=hoje)
    evidencias = EvidenciaAnalitica.objects.filter(autor=operador)[:12]
    analises = Analise.objects.filter(autor=operador).prefetch_related("evidencias")[:8]
    simulacoes = Simulacao.objects.filter(autor=operador).select_related("missao")[:8]
    if request.method == "POST":
        acao = request.POST.get("acao")
        try:
            if acao == "evidencia":
                registrar_evidencia(operador=operador, titulo=request.POST.get("titulo"), descricao=request.POST.get("descricao"), tipo=request.POST.get("tipo"), fonte=request.POST.get("fonte"), referencia=request.POST.get("referencia"), dados=json.loads(request.POST.get("dados") or "{}"), confianca=request.POST.get("confianca") or 100)
                messages.success(request, "Evidência registrada para uso auditável.")
            elif acao == "analise":
                ids = [int(value) for value in request.POST.getlist("evidencias")]
                criar_analise_deterministica(operador=operador, pergunta=request.POST.get("pergunta"), resumo=request.POST.get("resumo"), confianca=request.POST.get("confianca") or 0, evidencias=EvidenciaAnalitica.objects.filter(pk__in=ids))
                messages.success(request, "Análise determinística salva com suas evidências.")
            elif acao == "simulacao":
                validade = request.POST.get("validade_ate") or ""
                validade_ate = timezone.make_aware(datetime.fromisoformat(validade)) if validade else None
                salvar_simulacao(operador=operador, titulo=request.POST.get("titulo"), objetivo=request.POST.get("objetivo"), premissas=json.loads(request.POST.get("premissas") or "{}"), resultado=json.loads(request.POST.get("resultado") or "{}"), validade_ate=validade_ate)
                messages.success(request, "Simulação salva com validade própria.")
            elif acao == "promover":
                promover_simulacao_para_missao(simulacao=get_object_or_404(Simulacao, pk=request.POST.get("simulacao_id")), operador=operador)
                messages.success(request, "Simulação promovida para uma Missão explícita.")
            elif acao == "validar_analise":
                validar_analise(analise=get_object_or_404(Analise, pk=request.POST.get("analise_id")), operador=operador)
                messages.success(request, "Análise validada com suas evidências preservadas.")
        except (ValueError, TypeError, json.JSONDecodeError, ValidationError) as exc:
            messages.error(request, str(exc))
        return redirect("analytics_home")
    return render(request, "analytics/analytics.html", {"operador_atual": operador, "evidencias": evidencias, "analises": analises, "simulacoes": simulacoes, "relatorio": relatorio, "tipos_evidencia": TipoEvidencia.choices, "active": "analytics"})
