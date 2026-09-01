"""Contratos determinísticos para monitoramento operacional assistido."""

import hashlib
import json
from datetime import timedelta
from typing import Any

from django.conf import settings
from django.db.models import Q
from django.utils import timezone

from apps.auditoria.services import registrar_evento

from .gateway import estimar_custo
from .models import EventoAtividadeCognitiva, IntervencaoIA, TarefaCognitiva


TIPOS_ATIVIDADE_PERMITIDOS = {
    "tela_aberta",
    "pedido_aberto",
    "pedido_atividade",
    "intervencao_resposta",
}


def severidade_alerta(alerta: dict[str, Any]) -> str:
    """Classifica somente a partir dos fatos já calculados pelo backend."""
    nivel = int(alerta.get("nivel") or 0)
    texto = " ".join(str(alerta.get(campo) or "") for campo in ("tipo", "titulo", "mensagem")).casefold()
    if nivel >= 4:
        return "CRITICO"
    if "atras" in texto:
        return "ATRASADO"
    if nivel >= 3:
        return "RISCO"
    if nivel >= 2:
        return "ATENCAO"
    return "NORMAL"


def normalizar_alerta(alerta: dict[str, Any]) -> dict[str, Any]:
    campos = (
        "id", "pedido_id", "pedido_label", "cliente", "categoria_id", "categoria_nome",
        "tipo", "nivel", "criticidade", "titulo", "mensagem", "href", "acao_label",
        "exige_acao", "pode_dispensar", "acoes_disponiveis", "arquivo_id", "numero",
    )
    resultado = {campo: alerta.get(campo) for campo in campos}
    resultado["severidade"] = severidade_alerta(resultado)
    resultado["dedupe_key"] = ":".join(
        str(alerta.get(campo) or "") for campo in ("tipo", "pedido_id", "categoria_id", "arquivo_id")
    )
    return resultado


def fingerprint_contexto(valor: object) -> str:
    serializado = json.dumps(valor, ensure_ascii=False, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(serializado.encode("utf-8")).hexdigest()


def obter_contexto_atividade(*, operador, alertas: list[dict[str, Any]], agora=None) -> dict[str, Any]:
    agora = agora or timezone.now()
    janela = max(60, int(getattr(settings, "MHEIBOS_IA_ATIVIDADE_JANELA_SEGUNDOS", 1800)))
    inicio = agora - timedelta(seconds=janela)
    ids_pedidos = {str(item.get("pedido_id")) for item in alertas if item.get("pedido_id") is not None}
    eventos = list(
        EventoAtividadeCognitiva.objects.filter(
            operador=operador,
            ocorreu_em__gte=inicio,
        ).filter(Q(alvo_id__in=ids_pedidos) | Q(alvo_id=""))[:120]
    )
    por_pedido: dict[str, list[EventoAtividadeCognitiva]] = {}
    for evento in eventos:
        por_pedido.setdefault(evento.alvo_id, []).append(evento)

    pedidos = {}
    for pedido_id in ids_pedidos:
        relacionados = por_pedido.get(pedido_id, [])
        ultimo = relacionados[0] if relacionados else None
        pedidos[pedido_id] = {
            "usuario_ativo": bool(ultimo),
            "pedido_aberto_pelo_usuario": any(item.tipo == "pedido_aberto" for item in relacionados),
            "ultima_atividade_minutos": round((agora - ultimo.ocorreu_em).total_seconds() / 60, 1) if ultimo else None,
        }
    ultimo_geral = eventos[0] if eventos else None
    return {
        "usuario_ativo": bool(ultimo_geral),
        "ultima_atividade_minutos": round((agora - ultimo_geral.ocorreu_em).total_seconds() / 60, 1) if ultimo_geral else None,
        "pedidos": pedidos,
    }


def orçamento_disponivel(*, operador, fase: str = "triage", agora=None) -> tuple[bool, str]:
    """Aplica limites locais; zero significa sem limite configurado."""
    agora = agora or timezone.now()
    limite_diario = int(getattr(settings, "MHEIBOS_IA_LIMITE_DIARIO_API", 0) or 0)
    limite_mensal = int(getattr(settings, "MHEIBOS_IA_LIMITE_MENSAL_API", 0) or 0)
    limite_usuario = int(getattr(settings, "MHEIBOS_IA_MAX_AVALIACOES_USUARIO_HORA", 0) or 0)
    limite_intervencoes = int(getattr(settings, "MHEIBOS_IA_MAX_INTERVENCOES_USUARIO_HORA", 0) or 0)
    inicio_dia = agora.replace(hour=0, minute=0, second=0, microsecond=0)
    inicio_mes = inicio_dia.replace(day=1)
    tarefas = TarefaCognitiva.objects.filter(provider="gemini")
    tarefas_dia = tarefas.filter(criada_em__gte=inicio_dia)
    if limite_diario and tarefas_dia.count() >= limite_diario:
        return False, "LIMITE_DIARIO"
    if limite_mensal and tarefas.filter(criada_em__gte=inicio_mes).count() >= limite_mensal:
        return False, "LIMITE_MENSAL"
    if limite_usuario and tarefas_dia.filter(conversa__operador=operador, criada_em__gte=agora - timedelta(hours=1)).count() >= limite_usuario:
        return False, "LIMITE_USUARIO_HORA"
    if fase == "intervention" and limite_intervencoes and IntervencaoIA.objects.filter(operador=operador, criada_em__gte=agora - timedelta(hours=1)).count() >= limite_intervencoes:
        return False, "LIMITE_INTERVENCOES_USUARIO_HORA"
    return True, ""


def registrar_atividade(*, operador, tipo: str, alvo_tipo: str = "", alvo_id: str = "", dados: dict[str, Any] | None = None, ocorreu_em=None):
    if tipo not in TIPOS_ATIVIDADE_PERMITIDOS or not operador or not operador.ativo:
        return None
    evento = EventoAtividadeCognitiva.objects.create(
        operador=operador,
        tipo=tipo,
        alvo_tipo=str(alvo_tipo or "")[:48],
        alvo_id=str(alvo_id or "")[:80],
        dados=dados or {},
        ocorreu_em=ocorreu_em or timezone.now(),
    )
    return evento


def custo_para_resposta(*, modelo: str, tokens_input: int | None, tokens_output: int | None):
    return estimar_custo(modelo=modelo, tokens_input=tokens_input, tokens_output=tokens_output)


def auditar_intervencao(*, intervencao: IntervencaoIA, operador, acao: str, resultado: str):
    try:
        return registrar_evento(
            tipo="IntervencaoIAAtualizada",
            operador=operador,
            origem="cognicao",
            alvo_tipo="IntervencaoIA",
            alvo_id=str(intervencao.pk),
            acao=acao,
            valores_anteriores={},
            valores_posteriores={"estado": intervencao.estado, "resposta": intervencao.resposta_usuario},
            chave_idempotencia=f"intervencao-ia:{intervencao.pk}:{acao}:{intervencao.respondida_em or intervencao.exibida_em}",
            metadados={"resultado": resultado, "contexto_hash": intervencao.contexto_hash},
        )
    except Exception:
        return None
