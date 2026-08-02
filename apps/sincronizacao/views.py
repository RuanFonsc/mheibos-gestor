import json

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST

from apps.catalogo.permissions import operador_atual
from apps.catalogo.authentication import validar_senha_operador
from apps.auditoria.services import registrar_evento

from .models import EstacaoCliente, UnidadeSincronizacao
from .services import SincronizacaoInvalida, criar_estacao, incorporar_pedido_offline


def painel(request):
    operador = operador_atual(request)
    unidades = UnidadeSincronizacao.objects.select_related("pedido_local", "operador")
    if not operador.is_admin:
        unidades = unidades.filter(operador=operador)
    return render(request, "sincronizacao/painel.html", {"active": "sincronizacao", "unidades": unidades[:100]})


def estacoes(request):
    operador = operador_atual(request)
    if not operador.is_admin:
        return JsonResponse({"codigo": "ACESSO_NEGADO"}, status=403)
    segredo_novo = None
    erro = ""
    if request.method == "POST":
        senha = request.POST.get("senha_atual", "")
        if not validar_senha_operador(operador, senha):
            erro = "Senha atual incorreta. A Estacao nao foi criada."
        else:
            try:
                credencial = criar_estacao(nome=request.POST.get("nome", ""))
            except SincronizacaoInvalida as exc:
                erro = str(exc)
            else:
                segredo_novo = credencial.segredo
                registrar_evento(
                    tipo="EstacaoProvisionada",
                    operador=operador,
                    origem="gestor_web",
                    alvo_tipo="EstacaoCliente",
                    alvo_id=str(credencial.estacao.pk),
                    acao="provisionar_estacao",
                    valores_anteriores={},
                    valores_posteriores={
                        "nome": credencial.estacao.nome,
                        "ativa": True,
                    },
                    metadados={"reautenticada": True},
                )
    return render(
        request,
        "sincronizacao/estacoes.html",
        {
            "active": "sincronizacao",
            "estacoes": EstacaoCliente.objects.all(),
            "segredo_novo": segredo_novo,
            "erro": erro,
        },
    )


def _autenticar_estacao(request):
    try:
        estacao_id = request.headers["X-Mheibos-Station-ID"]
        segredo = request.headers.get("X-Mheibos-Station-Secret", "")
        if not segredo:
            esquema, segredo = request.headers["Authorization"].split(" ", 1)
            if esquema != "Bearer":
                return None
    except (KeyError, ValueError):
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


@csrf_exempt
@require_GET
def identidade_atual(request):
    if settings.MHEIBOS_RUNTIME_ROLE != "central":
        return JsonResponse({"codigo": "PAPEL_INVALIDO"}, status=409)
    estacao = _autenticar_estacao(request)
    if estacao is None:
        return JsonResponse({"codigo": "ESTACAO_NAO_AUTORIZADA"}, status=401)
    operador = operador_atual(request)
    if operador is None:
        return JsonResponse({"codigo": "SESSAO_NAO_AUTENTICADA"}, status=401)
    return JsonResponse(
        {
            "codigo": "IDENTIDADE_VALIDADA",
            "estacao_id": str(estacao.pk),
            "operador": {
                "nome": operador.nome,
                "email": operador.email,
                "papel": operador.papel,
                "codigo_origem_offline": operador.codigo_origem_offline,
            },
            "permissoes": {
                "pode_criar_pedido": operador.papel != "TEMPORARIO",
                "pode_cancelar_pedido": operador.pode_cancelar_pedido,
            },
            "versao_politica": settings.MHEIBOS_POLICY_VERSION,
        }
    )
