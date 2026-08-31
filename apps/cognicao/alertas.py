"""Gatilhos que encaminham alertas operacionais para a camada cognitiva."""

from django.conf import settings
from django.db import transaction
from django.utils import timezone

from apps.catalogo.models import OperadorGestor
from apps.catalogo.widget_data import alertas_operacionais

from .models import AlertaCognitiva, ConversaCognitiva, MensagemCognitiva, EstadoTarefaCognitiva, TarefaCognitiva


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
    return {campo: alerta.get(campo) for campo in CAMPOS_ALERTA_IA}


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


def encaminhar_alertas_para_ia(*, operador: OperadorGestor, limite: int = 100) -> list[TarefaCognitiva]:
    """Enfileira apenas alertas acionáveis novos, reabertos ou materialmente alterados."""
    if not operador or not operador.ativo or not ia_configurada_para_gatilhos():
        return []

    contrato = alertas_operacionais(operador=operador, limite=limite)
    atuais = [alerta for alerta in contrato["alertas"] if alerta.get("exige_acao")]
    chaves_atuais = {str(alerta["id"]) for alerta in atuais}
    tarefas: list[TarefaCognitiva] = []
    agora = timezone.now()

    with transaction.atomic():
        conversa = _conversa_alertas(operador)
        for alerta in atuais:
            chave = str(alerta["id"])
            snapshot = _snapshot(alerta)
            registro, criado = AlertaCognitiva.objects.select_for_update().get_or_create(
                operador=operador,
                chave=chave,
                defaults={"dados": snapshot, "ativa": True},
            )
            reaberto_ou_alterado = criado or not registro.ativa or registro.dados != snapshot
            if not reaberto_ou_alterado:
                continue

            tarefa_aberta = TarefaCognitiva.objects.filter(
                conversa=conversa,
                estado__in=(EstadoTarefaCognitiva.PENDENTE, EstadoTarefaCognitiva.PROCESSANDO),
                contexto__tipo="gatilho_alerta",
                contexto__alerta_chave=chave,
            ).exists()
            if tarefa_aberta:
                continue

            mensagem = MensagemCognitiva.objects.create(
                conversa=conversa,
                papel="SISTEMA",
                texto=f"Novo alerta operacional para análise: {alerta['pedido_label']} — {alerta['titulo']}.",
                metadados={"tipo": "gatilho_alerta", "alerta_chave": chave},
            )
            tarefa = TarefaCognitiva.objects.create(
                conversa=conversa,
                mensagem_usuario=mensagem,
                contexto={
                    "tipo": "gatilho_alerta",
                    "evento": "alerta_operacional_novo_ou_atualizado",
                    "alerta_chave": chave,
                    "alerta": snapshot,
                    "operador_id": operador.pk,
                    "texto": (
                        "Analise este alerta operacional acionável. Avise o operador de forma objetiva, "
                        "explique a decisão necessária e, se for seguro, proponha um comando para abrir o "
                        "pedido relacionado. Não altere dados nem invente informações."
                    ),
                    "interface": {
                        "rota": "/",
                        "titulo": "Início",
                        "campos": [],
                        "acoes": [{
                            "texto": str(alerta.get("acao_label") or "Abrir alerta"),
                            "tipo": "a",
                            "href": str(alerta.get("href") or ""),
                        }],
                    },
                },
            )
            registro.dados = snapshot
            registro.ativa = True
            registro.ultima_tarefa_em = agora
            registro.save(update_fields=["dados", "ativa", "ultima_tarefa_em", "atualizada_em"])
            tarefas.append(tarefa)

        registros_ausentes = AlertaCognitiva.objects.filter(operador=operador, ativa=True)
        if chaves_atuais:
            registros_ausentes = registros_ausentes.exclude(chave__in=chaves_atuais)
        registros_ausentes.update(ativa=False, atualizada_em=agora)

    return tarefas
