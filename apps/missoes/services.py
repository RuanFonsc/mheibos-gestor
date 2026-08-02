from django.core.exceptions import PermissionDenied, ValidationError
from django.db import transaction
from django.utils import timezone
from apps.auditoria.services import registrar_evento
from apps.catalogo.models import PapelOperador
from .models import EstadoMissao, Missao, OrigemMissao


@transaction.atomic
def criar_missao_individual_voluntaria(*, operador, titulo, objetivo, criterio_conclusao, resultado_esperado=""):
    if not operador or not operador.ativo or operador.papel == PapelOperador.TEMPORARIO:
        raise PermissionDenied("Somente uma identidade ativa pode criar uma missão.")
    campos = {"titulo": (titulo or "").strip(), "objetivo": (objetivo or "").strip(), "criterio_conclusao": (criterio_conclusao or "").strip()}
    if not all(campos.values()):
        raise ValidationError("Título, objetivo e critério de conclusão são obrigatórios.")
    missao = Missao.objects.create(**campos, resultado_esperado=(resultado_esperado or "").strip(), origem=OrigemMissao.VOLUNTARIA, estado=EstadoMissao.PLANEJADA, criador=operador, responsavel_principal=operador)
    registrar_evento(tipo="MissaoCriada", operador=operador, origem="missoes_web", alvo_tipo="Missao", alvo_id=str(missao.pk), acao="criar_missao_individual_voluntaria", valores_anteriores={}, valores_posteriores={"origem": missao.origem, "estado": missao.estado, "responsavel_principal_id": operador.pk})
    return missao


class TransicaoMissaoInvalida(ValidationError):
    pass


def _autorizar_responsavel(missao, operador):
    if not operador or not operador.ativo or missao.responsavel_principal_id != operador.pk:
        raise PermissionDenied("Somente o responsável pode alterar esta missão voluntária.")


def _obter_missao_bloqueada(missao, operador):
    atual = Missao.objects.select_for_update().get(pk=missao.pk)
    _autorizar_responsavel(atual, operador)
    return atual


def _evento_transicao(missao, operador, estado_anterior, tipo, acao, metadados=None):
    registrar_evento(
        tipo=tipo,
        operador=operador,
        origem="missoes_web",
        alvo_tipo="Missao",
        alvo_id=str(missao.pk),
        acao=acao,
        valores_anteriores={"estado": estado_anterior},
        valores_posteriores={"estado": missao.estado},
        metadados=metadados or {},
    )


@transaction.atomic
def iniciar_missao(*, missao, operador):
    missao = _obter_missao_bloqueada(missao, operador)
    if missao.estado == EstadoMissao.ATIVA:
        return missao
    if missao.estado != EstadoMissao.PLANEJADA:
        raise TransicaoMissaoInvalida("Somente uma missão planejada pode ser iniciada.")
    anterior = missao.estado
    missao.estado = EstadoMissao.ATIVA
    missao.iniciada_em = timezone.now()
    missao.save(update_fields=["estado", "iniciada_em", "atualizada_em"])
    _evento_transicao(missao, operador, anterior, "MissaoIniciada", "iniciar")
    return missao


@transaction.atomic
def pausar_missao(*, missao, operador, motivo):
    missao = _obter_missao_bloqueada(missao, operador)
    if missao.estado == EstadoMissao.PAUSADA:
        return missao
    if missao.estado != EstadoMissao.ATIVA:
        raise TransicaoMissaoInvalida("Somente uma missão ativa pode ser pausada.")
    motivo = (motivo or "").strip()
    if not motivo:
        raise ValidationError("O motivo da pausa é obrigatório.")
    anterior = missao.estado
    missao.estado = EstadoMissao.PAUSADA
    missao.pausada_em = timezone.now()
    missao.save(update_fields=["estado", "pausada_em", "atualizada_em"])
    _evento_transicao(missao, operador, anterior, "MissaoPausada", "pausar", {"motivo": motivo})
    return missao


@transaction.atomic
def retomar_missao(*, missao, operador, atualizacao=""):
    missao = _obter_missao_bloqueada(missao, operador)
    if missao.estado == EstadoMissao.ATIVA:
        return missao
    if missao.estado not in {EstadoMissao.PAUSADA, EstadoMissao.BLOQUEADA}:
        raise TransicaoMissaoInvalida("Somente missão pausada ou bloqueada pode ser retomada.")
    anterior = missao.estado
    agora = timezone.now()
    duracao = agora - missao.pausada_em if missao.pausada_em else None
    if duracao:
        missao.tempo_total_pausa += duracao
    missao.estado = EstadoMissao.ATIVA
    missao.pausada_em = None
    missao.motivo_bloqueio = ""
    missao.dependencia_bloqueio = ""
    missao.impacto_bloqueio = ""
    missao.ajuda_necessaria = ""
    missao.urgencia_bloqueio = ""
    missao.save(update_fields=["estado", "pausada_em", "tempo_total_pausa", "motivo_bloqueio", "dependencia_bloqueio", "impacto_bloqueio", "ajuda_necessaria", "urgencia_bloqueio", "atualizada_em"])
    _evento_transicao(missao, operador, anterior, "MissaoRetomada", "retomar", {"atualizacao": (atualizacao or "").strip(), "tempo_pausa_segundos": duracao.total_seconds() if duracao else 0})
    return missao


@transaction.atomic
def bloquear_missao(*, missao, operador, motivo, dependencia, impacto, ajuda_necessaria, urgencia):
    missao = _obter_missao_bloqueada(missao, operador)
    if missao.estado == EstadoMissao.BLOQUEADA:
        return missao
    if missao.estado not in {EstadoMissao.ATIVA, EstadoMissao.PAUSADA}:
        raise TransicaoMissaoInvalida("Somente missão em andamento pode registrar bloqueio.")
    dados = [str(valor or "").strip() for valor in (motivo, dependencia, impacto, ajuda_necessaria, urgencia)]
    if not all(dados):
        raise ValidationError("Motivo, dependência, impacto, ajuda e urgência são obrigatórios.")
    anterior = missao.estado
    missao.estado = EstadoMissao.BLOQUEADA
    missao.motivo_bloqueio, missao.dependencia_bloqueio, missao.impacto_bloqueio, missao.ajuda_necessaria, missao.urgencia_bloqueio = dados
    missao.save(update_fields=["estado", "motivo_bloqueio", "dependencia_bloqueio", "impacto_bloqueio", "ajuda_necessaria", "urgencia_bloqueio", "atualizada_em"])
    _evento_transicao(missao, operador, anterior, "MissaoBloqueada", "registrar_bloqueio", {"motivo": dados[0], "dependencia": dados[1], "impacto": dados[2], "ajuda_necessaria": dados[3], "urgencia": dados[4]})
    return missao


@transaction.atomic
def concluir_missao(*, missao, operador, resultado_alcancado, pendencias_remanescentes=""):
    missao = _obter_missao_bloqueada(missao, operador)
    if missao.estado == EstadoMissao.CONCLUIDA:
        return missao
    if missao.estado not in {EstadoMissao.ATIVA, EstadoMissao.EM_REVISAO}:
        raise TransicaoMissaoInvalida("Somente missão ativa ou em revisão pode ser concluída.")
    resultado = (resultado_alcancado or "").strip()
    if not resultado:
        raise ValidationError("O resultado alcançado é obrigatório.")
    if (pendencias_remanescentes or "").strip():
        raise ValidationError(
            "A missão não pode ser concluída enquanto houver obrigação remanescente sem destino formal."
        )
    anterior = missao.estado
    missao.estado = EstadoMissao.CONCLUIDA
    missao.resultado_alcancado = resultado
    missao.pendencias_remanescentes = ""
    missao.concluida_em = timezone.now()
    missao.concluida_por = operador
    missao.save(update_fields=["estado", "resultado_alcancado", "pendencias_remanescentes", "concluida_em", "concluida_por", "atualizada_em"])
    _evento_transicao(missao, operador, anterior, "MissaoConcluida", "concluir", {"resultado_alcancado": resultado, "pendencias_remanescentes": missao.pendencias_remanescentes})
    return missao
