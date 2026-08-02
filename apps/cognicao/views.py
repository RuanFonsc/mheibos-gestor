from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_POST

from apps.auditoria.services import registrar_evento
from apps.catalogo.permissions import operador_atual
from apps.operacao.projections import queryset_com_projecao
from apps.pedidos.models import Pedido

from .gateway import gateway_configurado
from .services import resumir_pedido


@require_POST
def resumo_pedido(request, pk):
    pedido = get_object_or_404(
        queryset_com_projecao(Pedido.objects.select_related("cliente")), pk=pk
    )
    operador = operador_atual(request)
    resposta = resumir_pedido(pedido=pedido, gateway=gateway_configurado())
    try:
        registrar_evento(
            tipo="AssistenciaCognitivaSolicitada",
            operador=operador,
            origem="gestor_web",
            alvo_tipo="Pedido",
            alvo_id=str(pedido.pk),
            acao="consultar_resumo_assistido",
            valores_anteriores={},
            valores_posteriores={"disponivel": resposta.disponivel},
            metadados={
                "provider": resposta.provider,
                "modelo": resposta.modelo,
                "codigo": resposta.codigo,
            },
        )
    except Exception:
        # Uma falha auxiliar de auditoria nao pode transformar IA em bloqueio operacional.
        pass
    return render(
        request,
        "cognicao/resumo_pedido.html",
        {"pedido": pedido, "resposta": resposta},
    )
