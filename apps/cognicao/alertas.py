"""Gatilhos que encaminham alertas operacionais para a camada cognitiva."""

from django.conf import settings
from django.db import transaction
from django.utils import timezone

from apps.catalogo.models import OperadorGestor
from apps.catalogo.widget_data import alertas_operacionais

from .models import AlertaCognitiva, ConversaCognitiva, MensagemCognitiva, EstadoTarefaCognitiva, TarefaCognitiva
from .monitoramento import fingerprint_contexto, normalizar_alerta, obter_contexto_atividade


CAMPOS_ALERTA_IA = (
    "id",
    "pedido_id",
    "pedido_label",
    "cliente",
    "categoria_id",
    "categoria_nome",
    "tipo",
    "nivel",
    "criticidade",
    "titulo",
    "mensagem",
    "href",
    "acao_label",
    "exige_acao",
    "pode_dispensar",
    "acoes_disponiveis",
    "arquivo_id",
    "numero",
)


def ia_configurada_para_gatilhos() -> bool:
    return bool(
        settings.MHEIBOS_IA_ENABLED
        and settings.MHEIBOS_IA_PROVIDER == "gemini"
        and settings.GEMINI_API_KEY
    )


def _snapshot(alerta: dict) -> dict:
    return normalizar_alerta(alerta)


def _conversa_alertas(operador: OperadorGestor) -> ConversaCognitiva:
    conversa = (
        ConversaCognitiva.objects.filter(
            operador=operador,
            origem="GESTOR",
            referencia_externa="alertas-operacionais",
            ativa=True,
        )
        .order_by("id")
        .first()
    )
    if conversa is not None:
        return conversa
    return ConversaCognitiva.objects.create(
        operador=operador,
        origem="GESTOR",
        referencia_externa="alertas-operacionais",
        titulo="Alertas operacionais",
        contexto={"finalidade": "encaminhamento_automatico_de_alertas"},
    )


def _severidade_maior(atual: str, anterior: str) -> bool:
    ordem = {"NORMAL": 1, "ATENCAO": 2, "RISCO": 3, "ATRASADO": 4, "CRITICO": 5}
    return ordem.get(atual, 0) > ordem.get(anterior, 0)


def _tem_tarefa_aberta(conversa, chaves: set[str]) -> bool:
    tarefas = TarefaCognitiva.objects.filter(
        conversa=conversa,
        estado__in=(EstadoTarefaCognitiva.PENDENTE, EstadoTarefaCognitiva.PROCESSANDO),
    ).only("contexto")
    return any(chaves.intersection(set(tarefa.contexto.get("alerta_chaves", []))) for tarefa in tarefas)


def _acoes_interface(alertas: list[dict]) -> list[dict]:
    return [
        {
            "texto": str(alerta.get("acao_label") or "Abrir alerta"),
            "tipo": "a",
            "href": str(alerta.get("href") or ""),
        }
        for alerta in alertas[:6]
        if alerta.get("href")
    ]


def encaminhar_alertas_para_ia(*, operador: OperadorGestor, limite: int = 100) -> list[TarefaCognitiva]:
    """Detecta deltas e enfileira pequenos lotes, sem consultar o LLM por alerta."""
    if not operador or not operador.ativo or not ia_configurada_para_gatilhos():
        return []

    contrato = alertas_operacionais(operador=operador, limite=limite)
    atuais = [normalizar_alerta(alerta) for alerta in contrato["alertas"] if alerta.get("exige_acao")]
    chaves_atuais = {str(alerta["id"]) for alerta in atuais}
    tarefas: list[TarefaCognitiva] = []
    agora = timezone.now()
    cooldown = max(0, int(getattr(settings, "MHEIBOS_IA_COOLDOWN_SEGUNDOS", 900)))

    with transaction.atomic():
        conversa = _conversa_alertas(operador)
        candidatos: list[dict] = []
        registros_candidatos: list[tuple[AlertaCognitiva, dict]] = []
        for alerta in atuais:
            chave = str(alerta["id"])
            snapshot = _snapshot(alerta)
            registro, criado = AlertaCognitiva.objects.select_for_update().get_or_create(
                operador=operador,
                chave=chave,
                defaults={
                    "dados": snapshot,
                    "ativa": True,
                    "fingerprint": fingerprint_contexto(snapshot),
                    "severidade": snapshot["severidade"],
                },
            )
            alterado = criado or not registro.ativa or registro.dados != snapshot
            if not alterado:
                continue
            cooldown_ativo = bool(
                registro.ultima_tarefa_em
                and (agora - registro.ultima_tarefa_em).total_seconds() < cooldown
            )
            reabertura_sem_mudanca = not criado and not registro.ativa and registro.dados == snapshot
            if cooldown_ativo and reabertura_sem_mudanca and not _severidade_maior(snapshot["severidade"], registro.severidade):
                continue
            candidatos.append(alerta)
            registros_candidatos.append((registro, snapshot))

        if candidatos:
            chaves_candidatas = {str(item["id"]) for item in candidatos}
            ids_pedidos = {str(item.get("pedido_id")) for item in candidatos}
            lote = [
                item for item in atuais
                if str(item["id"]) in chaves_candidatas or str(item.get("pedido_id")) in ids_pedidos
            ][:8]
            lote_chaves = {str(item["id"]) for item in lote}
            if not _tem_tarefa_aberta(conversa, lote_chaves):
                atividade = obter_contexto_atividade(operador=operador, alertas=lote, agora=agora)
                mensagem = MensagemCognitiva.objects.create(
                    conversa=conversa,
                    papel="SISTEMA",
                    texto=f"Novos alertas operacionais para triagem: {len(lote)} situação(ões).",
                    metadados={"tipo": "gatilho_alerta", "alerta_chaves": sorted(lote_chaves)},
                )
                principal = lote[0]
                tarefa = TarefaCognitiva.objects.create(
                    conversa=conversa,
                    mensagem_usuario=mensagem,
                    workload="triage",
                    contexto={
                        "tipo": "gatilho_alerta",
                        "evento": "alerta_operacional_novo_ou_atualizado",
                        "alerta_chave": str(principal.get("id") or ""),
                        "alerta_chaves": sorted(lote_chaves),
                        "alertas": lote,
                        "alerta": principal,
                        "atividade": atividade,
                        "operador_id": operador.pk,
                        "workload": "triage",
                        "texto": (
                            "Faça a triagem dos alertas operacionais. Decida se uma intervenção curta é útil "
                            "agora, considerando a atividade atual do usuário. Não altere dados, não invente "
                            "informações e não sugira ações fora dos links autorizados."
                        ),
                        "interface": {
                            "rota": "/",
                            "titulo": "Início",
                            "campos": [],
                            "acoes": _acoes_interface(lote),
                        },
                    },
                )
                for registro, snapshot in registros_candidatos:
                    if str(snapshot["id"]) not in lote_chaves:
                        continue
                    registro.dados = snapshot
                    registro.ativa = True
                    registro.fingerprint = fingerprint_contexto(snapshot)
                    registro.severidade = snapshot["severidade"]
                    registro.ultima_tarefa_em = agora
                    registro.resolvida_em = None
                    registro.resolvida_por = None
                    registro.save(update_fields=["dados", "ativa", "fingerprint", "severidade", "ultima_tarefa_em", "resolvida_em", "resolvida_por", "atualizada_em"])
                tarefas.append(tarefa)

        registros_ausentes = AlertaCognitiva.objects.filter(operador=operador, ativa=True)
        if chaves_atuais:
            registros_ausentes = registros_ausentes.exclude(chave__in=chaves_atuais)
        registros_ausentes.update(ativa=False, resolvida_em=agora, resolvida_por=operador, atualizada_em=agora)

    return tarefas
