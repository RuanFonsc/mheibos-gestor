from django.core.exceptions import PermissionDenied, ValidationError
from django.db import transaction
from django.utils import timezone
from apps.auditoria.services import registrar_evento
from apps.catalogo.models import PapelOperador
from .sugestoes import pedidos_atrasados_elegiveis
from .models import (
    EstadoMissao,
    EstadoParticipacao,
    Missao,
    ReferenciaPedidoMissao,
    OrigemMissao,
    PapelParticipacao,
    ParticipacaoMissao,
    TipoManifestacaoConvite,
    TipoMissao,
)


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


@transaction.atomic
def aceitar_sugestao_missao_pedidos_atrasados(
    *,
    operador,
    titulo,
    objetivo,
    criterio_conclusao,
    resultado_esperado="",
    pedido_ids=None,
):
    """Aceita uma proposta explícita e registra as referências oficiais."""


    if not operador or not operador.ativo or operador.papel == PapelOperador.TEMPORARIO:
        raise PermissionDenied("Somente uma identidade ativa pode aceitar uma sugestão.")
    pedidos_elegiveis = {
        pedido.pk: pedido
        for pedido in pedidos_atrasados_elegiveis(operador=operador)
    }
    ids_solicitados = {int(item) for item in (pedido_ids or [])}
    pedidos = [
        pedidos_elegiveis[pedido_id]
        for pedido_id in sorted(ids_solicitados)
        if pedido_id in pedidos_elegiveis
    ]
    if not pedidos:
        raise ValidationError("A proposta não possui mais pedidos atrasados elegíveis.")
    campos = {
        "titulo": (titulo or "").strip(),
        "objetivo": (objetivo or "").strip(),
        "criterio_conclusao": (criterio_conclusao or "").strip(),
    }
    if not all(campos.values()):
        raise ValidationError("Título, objetivo e critério de conclusão são obrigatórios.")
    missao = Missao.objects.create(
        **campos,
        resultado_esperado=(resultado_esperado or "").strip(),
        origem=OrigemMissao.SUGESTAO_ACEITA,
        estado=EstadoMissao.PLANEJADA,
        criador=operador,
        responsavel_principal=operador,
    )
    ReferenciaPedidoMissao.objects.bulk_create(
        [
            ReferenciaPedidoMissao(
                missao=missao,
                pedido=pedido,
                registrada_por=operador,
            )
            for pedido in pedidos
        ]
    )
    registrar_evento(
        tipo="MissaoCriada",
        operador=operador,
        origem="missoes_web",
        alvo_tipo="Missao",
        alvo_id=str(missao.pk),
        acao="aceitar_sugestao_pedidos_atrasados",
        valores_anteriores={},
        valores_posteriores={
            "origem": missao.origem,
            "estado": missao.estado,
            "responsavel_principal_id": operador.pk,
        },
        metadados={
            "tipo_sugestao": "pedidos_atrasados",
            "modo_sugestao": "deterministico",
            "pedidos_referenciados": [pedido.pk for pedido in pedidos],
        },
    )
    adicionar_tarefa_missao(
        missao=missao,
        operador=operador,
        titulo="Triar pedidos por urgência",
        descricao="Ordenar os pedidos referenciados por atraso, prazo e bloqueio visível.",
    )
    adicionar_tarefa_missao(
        missao=missao,
        operador=operador,
        titulo="Registrar a próxima ação de cada pedido",
        descricao="Atualizar ou encaminhar cada pedido somente após revisar sua situação oficial.",
    )
    adicionar_tarefa_missao(
        missao=missao,
        operador=operador,
        titulo="Revisar bloqueios com a equipe",
        descricao="Consolidar dependências que exigem decisão ou ajuda humana.",
    )
    return missao


@transaction.atomic
def criar_missao_coletiva_espontanea(
    *, operador, titulo, objetivo, criterio_conclusao, convidados, resultado_esperado=""
):
    if not operador or not operador.ativo or operador.papel == PapelOperador.TEMPORARIO:
        raise PermissionDenied("Somente uma identidade ativa pode criar uma missão coletiva.")
    convidados = list(dict.fromkeys(convidados or []))
    if not convidados:
        raise ValidationError("Uma missão coletiva precisa convidar pelo menos outra pessoa.")
    if operador in convidados or any(
        not convidado.ativo or convidado.papel == PapelOperador.TEMPORARIO
        for convidado in convidados
    ):
        raise ValidationError("Os convidados devem ser identidades ativas diferentes do criador.")
    campos = {
        "titulo": (titulo or "").strip(),
        "objetivo": (objetivo or "").strip(),
        "criterio_conclusao": (criterio_conclusao or "").strip(),
    }
    if not all(campos.values()):
        raise ValidationError("Título, objetivo e critério de conclusão são obrigatórios.")
    missao = Missao.objects.create(
        **campos,
        tipo=TipoMissao.COLETIVA_ESPONTANEA,
        resultado_esperado=(resultado_esperado or "").strip(),
        origem=OrigemMissao.VOLUNTARIA,
        estado=EstadoMissao.AGUARDANDO_ACEITE,
        criador=operador,
        responsavel_principal=operador,
    )
    ParticipacaoMissao.objects.create(
        missao=missao,
        operador=operador,
        papel=PapelParticipacao.LIDER,
        estado_participacao=EstadoParticipacao.ACEITO,
        respondido_em=timezone.now(),
    )
    registrar_evento(
        tipo="MissaoCriada",
        operador=operador,
        origem="missoes_web",
        alvo_tipo="Missao",
        alvo_id=str(missao.pk),
        acao="criar_missao_coletiva_espontanea",
        valores_anteriores={},
        valores_posteriores={"tipo": missao.tipo, "estado": missao.estado},
    )
    for convidado in convidados:
        convidar_participante(
            missao=missao,
            convidado=convidado,
            operador=operador,
            papel=PapelParticipacao.PARTICIPANTE,
        )
    return missao


@transaction.atomic
def convidar_participante(*, missao, convidado, operador, papel=PapelParticipacao.PARTICIPANTE):
    missao = _obter_missao_bloqueada(missao, operador)
    if missao.tipo != TipoMissao.COLETIVA_ESPONTANEA:
        raise ValidationError("Convite voluntário pertence somente à missão coletiva espontânea.")
    if missao.estado in {EstadoMissao.CONCLUIDA, EstadoMissao.CANCELADA, EstadoMissao.ARQUIVADA}:
        raise ValidationError("Missão encerrada não recebe novos convites.")
    if convidado.pk == operador.pk or not convidado.ativo or convidado.papel == PapelOperador.TEMPORARIO:
        raise ValidationError("Selecione outra identidade ativa para o convite.")
    if papel not in {PapelParticipacao.PARTICIPANTE, PapelParticipacao.OBSERVADOR, PapelParticipacao.APROVADOR}:
        raise ValidationError("Papel de convite inválido.")
    existente = ParticipacaoMissao.objects.select_for_update().filter(
        missao=missao, operador=convidado, encerrado_em__isnull=True
    ).first()
    if existente:
        return existente
    participacao = ParticipacaoMissao.objects.create(
        missao=missao,
        operador=convidado,
        papel=papel,
        estado_participacao=EstadoParticipacao.CONVIDADO,
        convidado_por=operador,
        convidado_em=timezone.now(),
    )
    registrar_evento(
        tipo="ParticipanteConvidado",
        operador=operador,
        origem="missoes_web",
        alvo_tipo="Missao",
        alvo_id=str(missao.pk),
        acao="convidar_participante",
        valores_anteriores={},
        valores_posteriores={"participacao_id": str(participacao.pk), "operador_id": convidado.pk, "papel": papel},
    )
    return participacao


@transaction.atomic
def responder_convite(*, participacao, operador, aceitar):
    participacao = ParticipacaoMissao.objects.select_for_update().select_related("missao").get(pk=participacao.pk)
    if participacao.operador_id != operador.pk or not operador.ativo:
        raise PermissionDenied("Somente a pessoa convidada pode responder ao convite.")
    estado_alvo = EstadoParticipacao.ACEITO if aceitar else EstadoParticipacao.RECUSADO
    if participacao.estado_participacao == estado_alvo:
        return participacao
    if participacao.estado_participacao != EstadoParticipacao.CONVIDADO:
        raise ValidationError("Este convite não está mais aguardando resposta.")
    missao = Missao.objects.select_for_update().get(pk=participacao.missao_id)
    if missao.estado in {EstadoMissao.CONCLUIDA, EstadoMissao.CANCELADA, EstadoMissao.ARQUIVADA}:
        raise ValidationError("Convite de missão encerrada não pode ser aceito ou recusado agora.")
    participacao.estado_participacao = estado_alvo
    participacao.respondido_em = timezone.now()
    if not aceitar:
        participacao.encerrado_em = participacao.respondido_em
    participacao.save(update_fields=["estado_participacao", "respondido_em", "encerrado_em", "atualizada_em"])
    estado_anterior = missao.estado
    if aceitar and missao.estado == EstadoMissao.AGUARDANDO_ACEITE:
        missao.estado = EstadoMissao.PLANEJADA
        missao.save(update_fields=["estado", "atualizada_em"])
    registrar_evento(
        tipo="ConviteAceito" if aceitar else "ConviteRecusado",
        operador=operador,
        origem="missoes_web",
        alvo_tipo="Missao",
        alvo_id=str(missao.pk),
        acao="responder_convite",
        valores_anteriores={"estado_participacao": EstadoParticipacao.CONVIDADO, "estado_missao": estado_anterior},
        valores_posteriores={"estado_participacao": estado_alvo, "estado_missao": missao.estado},
        metadados={"participacao_id": str(participacao.pk)},
    )
    return participacao


@transaction.atomic
def manifestar_convite(*, participacao, operador, tipo, texto):
    participacao = ParticipacaoMissao.objects.select_for_update().get(pk=participacao.pk)
    if participacao.operador_id != operador.pk or not operador.ativo:
        raise PermissionDenied("Somente a pessoa convidada pode se manifestar.")
    if participacao.estado_participacao != EstadoParticipacao.CONVIDADO:
        raise ValidationError("Somente convite pendente aceita manifestação.")
    if tipo not in TipoManifestacaoConvite.values or not (texto or "").strip():
        raise ValidationError("Informe o tipo e o conteúdo da manifestação.")
    participacao.manifestacao_tipo = tipo
    participacao.manifestacao_texto = texto.strip()
    participacao.save(update_fields=["manifestacao_tipo", "manifestacao_texto", "atualizada_em"])
    registrar_evento(
        tipo="ConviteManifestado",
        operador=operador,
        origem="missoes_web",
        alvo_tipo="Missao",
        alvo_id=str(participacao.missao_id),
        acao="manifestar_convite",
        valores_anteriores={},
        valores_posteriores={"tipo": tipo},
        metadados={"participacao_id": str(participacao.pk), "texto": participacao.manifestacao_texto},
    )
    return participacao


@transaction.atomic
def sair_missao_espontanea(*, participacao, operador, confirmacao, motivo):
    participacao = ParticipacaoMissao.objects.select_for_update().select_related("missao").get(pk=participacao.pk)
    if participacao.operador_id != operador.pk or not operador.ativo:
        raise PermissionDenied("Somente o próprio participante pode sair voluntariamente.")
    if participacao.missao.tipo != TipoMissao.COLETIVA_ESPONTANEA:
        raise PermissionDenied("Missão atribuída não permite saída unilateral.")
    if participacao.missao.estado in {
        EstadoMissao.CONCLUIDA,
        EstadoMissao.CANCELADA,
        EstadoMissao.ARQUIVADA,
    }:
        raise ValidationError("Participação histórica de missão encerrada não pode ser alterada.")
    if participacao.papel == PapelParticipacao.LIDER:
        raise ValidationError("O líder precisa transferir a liderança antes de sair.")
    if participacao.estado_participacao == EstadoParticipacao.SAIU:
        return participacao
    if participacao.estado_participacao != EstadoParticipacao.ACEITO:
        raise ValidationError("Somente participante ativo pode sair da missão.")
    if (confirmacao or "").strip().upper() != "SAIR" or not (motivo or "").strip():
        raise ValidationError("Confirme SAIR e registre o motivo após revisar o impacto.")
    participacao.estado_participacao = EstadoParticipacao.SAIU
    participacao.encerrado_em = timezone.now()
    participacao.motivo_saida = motivo.strip()
    participacao.impacto_saida_confirmado = True
    participacao.save(update_fields=["estado_participacao", "encerrado_em", "motivo_saida", "impacto_saida_confirmado", "atualizada_em"])
    registrar_evento(
        tipo="ParticipanteSaiuVoluntariamente",
        operador=operador,
        origem="missoes_web",
        alvo_tipo="Missao",
        alvo_id=str(participacao.missao_id),
        acao="sair_voluntariamente",
        valores_anteriores={"estado_participacao": EstadoParticipacao.ACEITO},
        valores_posteriores={"estado_participacao": EstadoParticipacao.SAIU},
        metadados={"participacao_id": str(participacao.pk), "motivo": participacao.motivo_saida, "impacto_confirmado": True},
    )
    return participacao


class TransicaoMissaoInvalida(ValidationError):
    pass


def _autorizar_responsavel(missao, operador):
    if not operador or not operador.ativo or missao.responsavel_principal_id != operador.pk:
        raise PermissionDenied("Somente o responsável pode alterar esta missão voluntária.")


def _obter_missao_bloqueada(missao, operador):
    atual = Missao.objects.select_for_update().get(pk=missao.pk)
    _autorizar_responsavel(atual, operador)
    return atual


def _autorizar_colaborador(missao, operador):
    if not operador or not operador.ativo:
        raise PermissionDenied("Identidade inválida para colaborar na missão.")
    if missao.responsavel_principal_id == operador.pk or missao.criador_id == operador.pk:
        return
    if not missao.participacoes.filter(
        operador=operador,
        estado_participacao__in=[EstadoParticipacao.ACEITO, EstadoParticipacao.ATRIBUIDO],
        encerrado_em__isnull=True,
    ).exists():
        raise PermissionDenied("Somente participantes ativos podem colaborar na missão.")


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
    if missao.participacoes.filter(
        estado_participacao=EstadoParticipacao.CONVIDADO,
        encerrado_em__isnull=True,
    ).exists():
        raise ValidationError("Resolva os convites pendentes antes de concluir a missão.")
    anterior = missao.estado
    missao.estado = EstadoMissao.CONCLUIDA
    missao.resultado_alcancado = resultado
    missao.pendencias_remanescentes = ""
    missao.concluida_em = timezone.now()
    missao.concluida_por = operador
    missao.save(update_fields=["estado", "resultado_alcancado", "pendencias_remanescentes", "concluida_em", "concluida_por", "atualizada_em"])
    _evento_transicao(missao, operador, anterior, "MissaoConcluida", "concluir", {"resultado_alcancado": resultado, "pendencias_remanescentes": missao.pendencias_remanescentes})
    return missao


@transaction.atomic
def criar_missao_atribuida(
    *, gerente, responsavel, titulo, objetivo, criterio_conclusao, resultado_esperado=""
):
    if not gerente or not gerente.ativo or not gerente.is_admin:
        raise PermissionDenied("A atribuição de missão exige um gerente ou administrador ativo.")
    if not responsavel or not responsavel.ativo or responsavel.papel == PapelOperador.TEMPORARIO:
        raise ValidationError("O responsável principal deve ser uma identidade ativa válida.")
    campos = {
        "titulo": (titulo or "").strip(),
        "objetivo": (objetivo or "").strip(),
        "criterio_conclusao": (criterio_conclusao or "").strip(),
    }
    if not all(campos.values()):
        raise ValidationError("Título, objetivo e critério de conclusão são obrigatórios.")
    missao = Missao.objects.create(
        **campos,
        tipo=TipoMissao.INDIVIDUAL_ATRIBUIDA,
        resultado_esperado=(resultado_esperado or "").strip(),
        origem=OrigemMissao.ADMINISTRATIVA,
        estado=EstadoMissao.PLANEJADA,
        criador=gerente,
        autoridade_responsavel=gerente,
        responsavel_principal=responsavel,
    )
    ParticipacaoMissao.objects.create(
        missao=missao,
        operador=responsavel,
        papel=PapelParticipacao.PARTICIPANTE,
        estado_participacao=EstadoParticipacao.ATRIBUIDO,
        respondido_em=timezone.now(),
    )
    registrar_evento(
        tipo="MissaoAtribuidaCriada",
        operador=gerente,
        origem="missoes_web",
        alvo_tipo="Missao",
        alvo_id=str(missao.pk),
        acao="criar_missao_atribuida",
        valores_anteriores={},
        valores_posteriores={
            "autoridade_id": gerente.pk,
            "responsavel_principal_id": responsavel.pk,
            "tipo": missao.tipo,
        },
    )
    return missao


@transaction.atomic
def adicionar_tarefa_missao(*, missao, operador, titulo, descricao="", responsavel=None):
    missao = Missao.objects.select_for_update().get(pk=missao.pk)
    _autorizar_colaborador(missao, operador)
    if missao.estado in {EstadoMissao.CONCLUIDA, EstadoMissao.CANCELADA, EstadoMissao.ARQUIVADA}:
        raise ValidationError("Não é possível adicionar tarefa a uma missão encerrada.")
    titulo = (titulo or "").strip()
    if not titulo:
        raise ValidationError("O título da tarefa é obrigatório.")
    ordem_atual = missao.tarefas.count() + 1
    from .models import TarefaMissao, EstadoTarefaMissao
    tarefa = TarefaMissao.objects.create(
        missao=missao,
        titulo=titulo,
        descricao=(descricao or "").strip(),
        responsavel=responsavel or operador,
        ordem=ordem_atual,
    )
    registrar_evento(
        tipo="TarefaMissaoAdicionada",
        operador=operador,
        origem="missoes_web",
        alvo_tipo="TarefaMissao",
        alvo_id=str(tarefa.pk),
        acao="adicionar_tarefa_missao",
        valores_anteriores={},
        valores_posteriores={"missao_id": str(missao.pk), "titulo": titulo},
    )
    return tarefa


@transaction.atomic
def concluir_tarefa_missao(*, tarefa, operador):
    from .models import TarefaMissao, EstadoTarefaMissao
    tarefa = TarefaMissao.objects.select_for_update().select_related("missao").get(pk=tarefa.pk)
    _autorizar_colaborador(tarefa.missao, operador)
    if tarefa.responsavel_id and tarefa.responsavel_id != operador.pk and tarefa.missao.responsavel_principal_id != operador.pk:
        raise PermissionDenied("Somente o responsável da tarefa ou da missão pode concluí-la.")
    if tarefa.estado == EstadoTarefaMissao.CONCLUIDA:
        return tarefa
    tarefa.estado = EstadoTarefaMissao.CONCLUIDA
    tarefa.concluida_em = timezone.now()
    tarefa.concluida_por = operador
    tarefa.save(update_fields=["estado", "concluida_em", "concluida_por", "atualizada_em"])
    registrar_evento(
        tipo="TarefaMissaoConcluida",
        operador=operador,
        origem="missoes_web",
        alvo_tipo="TarefaMissao",
        alvo_id=str(tarefa.pk),
        acao="concluir_tarefa_missao",
        valores_anteriores={"estado": EstadoTarefaMissao.PENDENTE},
        valores_posteriores={"estado": EstadoTarefaMissao.CONCLUIDA},
    )
    return tarefa


@transaction.atomic
def adicionar_nota_missao(*, missao, operador, titulo, conteudo):
    missao = Missao.objects.select_for_update().get(pk=missao.pk)
    _autorizar_colaborador(missao, operador)
    if missao.estado in {EstadoMissao.CONCLUIDA, EstadoMissao.CANCELADA, EstadoMissao.ARQUIVADA}:
        raise ValidationError("Não é possível adicionar notas a uma missão encerrada.")
    titulo = (titulo or "").strip()
    conteudo = (conteudo or "").strip()
    if not titulo or not conteudo:
        raise ValidationError("Título e conteúdo da nota são obrigatórios.")
    from .models import NotaMissao
    nota = NotaMissao.objects.create(
        missao=missao,
        titulo=titulo,
        conteudo=conteudo,
        autor=operador,
    )
    registrar_evento(
        tipo="NotaMissaoAdicionada",
        operador=operador,
        origem="missoes_web",
        alvo_tipo="NotaMissao",
        alvo_id=str(nota.pk),
        acao="adicionar_nota_missao",
        valores_anteriores={},
        valores_posteriores={"missao_id": str(missao.pk), "titulo": titulo},
    )
    return nota


@transaction.atomic
def enviar_mensagem_chat_missao(*, missao, operador, conteudo):
    missao = Missao.objects.select_for_update().get(pk=missao.pk)
    _autorizar_colaborador(missao, operador)
    if missao.estado in {EstadoMissao.CONCLUIDA, EstadoMissao.CANCELADA, EstadoMissao.ARQUIVADA}:
        raise ValidationError("Não é possível enviar mensagens em uma missão encerrada.")
    conteudo = (conteudo or "").strip()
    if not conteudo:
        raise ValidationError("O conteúdo da mensagem é obrigatório.")
    from .models import MensagemChatMissao
    mensagem = MensagemChatMissao.objects.create(
        missao=missao,
        autor=operador,
        conteudo=conteudo,
    )
    registrar_evento(
        tipo="MensagemChatMissaoEnviada",
        operador=operador,
        origem="missoes_web",
        alvo_tipo="MensagemChatMissao",
        alvo_id=str(mensagem.pk),
        acao="enviar_mensagem_chat_missao",
        valores_anteriores={},
        valores_posteriores={"missao_id": str(missao.pk)},
    )
    return mensagem


@transaction.atomic
def solicitar_revisao_missao(*, missao, operador):
    missao = _obter_missao_bloqueada(missao, operador)
    if missao.estado == EstadoMissao.EM_REVISAO:
        return missao
    if missao.estado != EstadoMissao.ATIVA:
        raise TransicaoMissaoInvalida("Somente missão ativa pode ser enviada para revisão.")
    anterior = missao.estado
    missao.estado = EstadoMissao.EM_REVISAO
    missao.save(update_fields=["estado", "atualizada_em"])
    _evento_transicao(missao, operador, anterior, "MissaoEnviadaParaRevisao", "solicitar_revisao")
    return missao
