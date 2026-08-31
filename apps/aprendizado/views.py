import json

from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from apps.aprendizado.models import AmostraTreinamento, ConversaAprendizado
from apps.aprendizado.services import EXPORT_CONVERSAS_FILE, exportar_conversas_uteis_json, registrar_evento_evolution


META_TREINAMENTO = 1000


def _percentual(valor, meta):
    if not meta:
        return 0
    return min(100, round((valor / meta) * 100, 1))


def aprendizado_home(request):
    total = ConversaAprendizado.objects.count()
    uteis = ConversaAprendizado.objects.filter(util_para_treinamento=True).count()
    amostras = AmostraTreinamento.objects.filter(pronta=True).count()
    leads = ConversaAprendizado.objects.filter(tem_lead=True).count()
    reclamacoes = ConversaAprendizado.objects.filter(tem_reclamacao=True).count()
    pedidos = ConversaAprendizado.objects.filter(tem_sinal_pedido=True).count()
    por_tipo = list(
        AmostraTreinamento.objects.values("tipo")
        .annotate(total=Count("id"))
        .order_by("tipo")
    )
    conversas = ConversaAprendizado.objects.order_by("-ultima_mensagem_em", "-atualizado_em")[:20]
    progresso_treinamento = _percentual(uteis, META_TREINAMENTO)
    faltantes = max(0, META_TREINAMENTO - uteis)
    return render(
        request,
        "aprendizado/home.html",
        {
            "active": "aprendizado",
            "total": total,
            "uteis": uteis,
            "amostras": amostras,
            "leads": leads,
            "reclamacoes": reclamacoes,
            "pedidos": pedidos,
            "meta_treinamento": META_TREINAMENTO,
            "progresso_treinamento": progresso_treinamento,
            "faltantes": faltantes,
            "pronto_treino": uteis >= META_TREINAMENTO,
            "por_tipo": por_tipo,
            "conversas": conversas,
            "arquivo_export": str(EXPORT_CONVERSAS_FILE),
        },
    )


def aprendizado_exportar_json(request):
    payload = exportar_conversas_uteis_json()
    return JsonResponse(payload, json_dumps_params={"ensure_ascii": False, "indent": 2})


def _json_body(request):
    raw = request.body or b"{}"
    for encoding in ("utf-8-sig", request.encoding, "cp1252"):
        if not encoding:
            continue
        try:
            return json.loads(raw.decode(encoding) or "{}")
        except UnicodeDecodeError:
            continue
    return json.loads(raw.decode("utf-8", errors="replace") or "{}")


@csrf_exempt
@require_http_methods(["GET", "POST"])
def evolution_webhook(request):
    if request.method == "GET":
        return JsonResponse({"ok": True, "modulo": "Mheibos Aprendizado"})
    try:
        payload = _json_body(request)
    except json.JSONDecodeError:
        return JsonResponse({"ok": False, "erro": "JSON invalido"}, status=400)
    conversa = registrar_evento_evolution(payload)
    from apps.cognicao.whatsapp import espelhar_mensagem_whatsapp

    conversa_cognitiva = espelhar_mensagem_whatsapp(conversa)
    return JsonResponse(
        {
            "ok": True,
            "conversa_id": conversa.pk,
            "contexto_cognitivo_id": conversa_cognitiva.pk,
            "total_mensagens": conversa.total_mensagens,
            "util_para_treinamento": conversa.util_para_treinamento,
        }
    )
