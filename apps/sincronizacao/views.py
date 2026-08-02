import json

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from apps.catalogo.permissions import operador_atual

from .models import EstacaoCliente, UnidadeSincronizacao
from .services import SincronizacaoInvalida, incorporar_pedido_offline


def painel(request):
    operador = operador_atual(request)
    unidades = UnidadeSincronizacao.objects.select_related("pedido_local", "operador")
    if not operador.is_admin:
        unidades = unidades.filter(operador=operador)
    return render(request, "sincronizacao/painel.html", {"active": "sincronizacao", "unidades": unidades[:100]})


def _autenticar_estacao(request):
    try:
        estacao_id = request.headers["X-Mheibos-Station-ID"]
        esquema, segredo = request.headers["Authorization"].split(" ", 1)
    except (KeyError, ValueError):
        return None
    if esquema != "Bearer":
        return None
    estacao = EstacaoCliente.objects.filter(pk=estacao_id, ativa=True).first()
    if estacao and estacao.verifica_segredo(segredo):
        return estacao
    return None


@csrf_exempt
@require_POST
def incorporar(request):
    if settings.MHEIBOS_RUNTIME_ROLE != "central":
        return JsonResponse({"codigo": "PAPEL_INVALIDO"}, status=409)
    if int(request.headers.get("Content-Length", "0") or 0) > 2_000_000:
        return JsonResponse({"codigo": "PACOTE_EXCESSIVO"}, status=413)
    estacao = _autenticar_estacao(request)
    if estacao is None:
        return JsonResponse({"codigo": "ESTACAO_NAO_AUTORIZADA"}, status=401)
    try:
        envelope = json.loads(request.body)
        if not isinstance(envelope, dict):
            raise ValueError
    except (json.JSONDecodeError, UnicodeDecodeError, ValueError):
        return JsonResponse({"codigo": "PACOTE_INVALIDO"}, status=400)
    try:
        resultado = incorporar_pedido_offline(
            envelope, estacao_autenticada=estacao
        )
    except SincronizacaoInvalida as exc:
        return JsonResponse(
            {"codigo": "INCORPORACAO_RECUSADA", "motivo": str(exc)}, status=422
        )
    return JsonResponse(
        {
            "codigo": "JA_INCORPORADO" if resultado.repetida else "INCORPORADO",
            "pedido_global_id": resultado.pedido.pk,
            "identificador_offline": str(resultado.pedido.identificador_offline),
        },
        status=200 if resultado.repetida else 201,
    )
