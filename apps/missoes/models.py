import uuid
from datetime import timedelta
from django.db import models
from django.db.models import Q


class OrigemMissao(models.TextChoices):
    VOLUNTARIA = "VOLUNTARIA", "Voluntária"
    ADMINISTRATIVA = "ADMINISTRATIVA", "Administrativa"
    IA_ACEITA = "IA_ACEITA", "Sugestão da IA aceita"


class EstadoMissao(models.TextChoices):
    PROPOSTA = "PROPOSTA", "Proposta"
    AGUARDANDO_ACEITE = "AGUARDANDO_ACEITE", "Aguardando aceite"
    PLANEJADA = "PLANEJADA", "Planejada"
    ATIVA = "ATIVA", "Ativa"
    PAUSADA = "PAUSADA", "Pausada"
    BLOQUEADA = "BLOQUEADA", "Bloqueada"
    EM_REVISAO = "EM_REVISAO", "Em revisão"
    CONCLUIDA = "CONCLUIDA", "Concluída"
    CANCELADA = "CANCELADA", "Cancelada"
    ARQUIVADA = "ARQUIVADA", "Arquivada"


class TipoMissao(models.TextChoices):
    INDIVIDUAL_VOLUNTARIA = "INDIVIDUAL_VOLUNTARIA", "Individual voluntária"
    INDIVIDUAL_ATRIBUIDA = "INDIVIDUAL_ATRIBUIDA", "Individual atribuída"
    COLETIVA_ESPONTANEA = "COLETIVA_ESPONTANEA", "Coletiva espontânea"
    COLETIVA_ATRIBUIDA = "COLETIVA_ATRIBUIDA", "Coletiva atribuída"


class PapelParticipacao(models.TextChoices):
    LIDER = "LIDER", "Líder"
    PARTICIPANTE = "PARTICIPANTE", "Participante"
    OBSERVADOR = "OBSERVADOR", "Observador autorizado"
    APROVADOR = "APROVADOR", "Aprovador"


class EstadoParticipacao(models.TextChoices):
    CONVIDADO = "CONVIDADO", "Convidado"
    ACEITO = "ACEITO", "Aceito"
    RECUSADO = "RECUSADO", "Recusado"
    SAIU = "SAIU", "Saiu voluntariamente"
    REMOVIDO = "REMOVIDO", "Removido pela autoridade"
    ATRIBUIDO = "ATRIBUIDO", "Atribuído formalmente"


class TipoManifestacaoConvite(models.TextChoices):
    MAIS_INFORMACOES = "MAIS_INFORMACOES", "Pediu mais informações"
    AJUSTE_PARTICIPACAO = "AJUSTE_PARTICIPACAO", "Sugeriu ajuste de participação"


class Missao(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    titulo = models.CharField(max_length=160)
    tipo = models.CharField(
        max_length=32,
        choices=TipoMissao.choices,
        default=TipoMissao.INDIVIDUAL_VOLUNTARIA,
    )
    objetivo = models.TextField()
    criterio_conclusao = models.TextField()
    resultado_esperado = models.TextField(blank=True)
    origem = models.CharField(max_length=24, choices=OrigemMissao.choices)
    estado = models.CharField(max_length=24, choices=EstadoMissao.choices)
    criador = models.ForeignKey("catalogo.OperadorGestor", related_name="missoes_criadas", on_delete=models.PROTECT)
    autoridade_responsavel = models.ForeignKey(
        "catalogo.OperadorGestor",
        related_name="missoes_sob_autoridade",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
    )
    responsavel_principal = models.ForeignKey("catalogo.OperadorGestor", related_name="missoes_responsaveis", on_delete=models.PROTECT)
    iniciada_em = models.DateTimeField(null=True, blank=True)
    pausada_em = models.DateTimeField(null=True, blank=True)
    tempo_total_pausa = models.DurationField(default=timedelta)
    motivo_bloqueio = models.TextField(blank=True)
    dependencia_bloqueio = models.TextField(blank=True)
    impacto_bloqueio = models.TextField(blank=True)
    ajuda_necessaria = models.TextField(blank=True)
    urgencia_bloqueio = models.CharField(max_length=80, blank=True)
    resultado_alcancado = models.TextField(blank=True)
    pendencias_remanescentes = models.TextField(blank=True)
    concluida_em = models.DateTimeField(null=True, blank=True)
    concluida_por = models.ForeignKey(
        "catalogo.OperadorGestor",
        related_name="missoes_concluidas",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
    )
    criada_em = models.DateTimeField(auto_now_add=True)
    atualizada_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-atualizada_em", "-criada_em"]

    def __str__(self):
        return self.titulo


class ParticipacaoMissao(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    missao = models.ForeignKey(Missao, related_name="participacoes", on_delete=models.PROTECT)
    operador = models.ForeignKey(
        "catalogo.OperadorGestor", related_name="participacoes_missao", on_delete=models.PROTECT
    )
    papel = models.CharField(max_length=24, choices=PapelParticipacao.choices)
    estado_participacao = models.CharField(max_length=24, choices=EstadoParticipacao.choices)
    convidado_por = models.ForeignKey(
        "catalogo.OperadorGestor",
        related_name="convites_missao_emitidos",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
    )
    convidado_em = models.DateTimeField(null=True, blank=True)
    respondido_em = models.DateTimeField(null=True, blank=True)
    encerrado_em = models.DateTimeField(null=True, blank=True)
    manifestacao_tipo = models.CharField(
        max_length=32, choices=TipoManifestacaoConvite.choices, blank=True
    )
    manifestacao_texto = models.TextField(blank=True)
    motivo_saida = models.TextField(blank=True)
    impacto_saida_confirmado = models.BooleanField(default=False)
    criada_em = models.DateTimeField(auto_now_add=True)
    atualizada_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["criada_em"]
        constraints = [
            models.UniqueConstraint(
                fields=["missao", "operador"],
                condition=Q(encerrado_em__isnull=True),
                name="missoes_participacao_corrente_unica",
            )
        ]


class EstadoTarefaMissao(models.TextChoices):
    PENDENTE = "PENDENTE", "Pendente"
    EM_ANDAMENTO = "EM_ANDAMENTO", "Em andamento"
    CONCLUIDA = "CONCLUIDA", "Concluída"
    CANCELADA = "CANCELADA", "Cancelada"


class TarefaMissao(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    missao = models.ForeignKey(Missao, related_name="tarefas", on_delete=models.PROTECT)
    titulo = models.CharField(max_length=160)
    descricao = models.TextField(blank=True)
    responsavel = models.ForeignKey(
        "catalogo.OperadorGestor",
        related_name="tarefas_missao_responsaveis",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
    )
    estado = models.CharField(
        max_length=24,
        choices=EstadoTarefaMissao.choices,
        default=EstadoTarefaMissao.PENDENTE,
    )
    ordem = models.PositiveIntegerField(default=0)
    concluida_em = models.DateTimeField(null=True, blank=True)
    concluida_por = models.ForeignKey(
        "catalogo.OperadorGestor",
        related_name="tarefas_missao_concluidas",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
    )
    criada_em = models.DateTimeField(auto_now_add=True)
    atualizada_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["ordem", "criada_em"]


class NotaMissao(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    missao = models.ForeignKey(Missao, related_name="notas", on_delete=models.PROTECT)
    titulo = models.CharField(max_length=160)
    conteudo = models.TextField()
    autor = models.ForeignKey(
        "catalogo.OperadorGestor",
        related_name="notas_missao_autor",
        on_delete=models.PROTECT,
    )
    criada_em = models.DateTimeField(auto_now_add=True)
    atualizada_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-atualizada_em"]


class MensagemChatMissao(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    missao = models.ForeignKey(Missao, related_name="mensagens_chat", on_delete=models.PROTECT)
    autor = models.ForeignKey(
        "catalogo.OperadorGestor",
        related_name="mensagens_chat_missao",
        on_delete=models.PROTECT,
    )
    conteudo = models.TextField()
    criada_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["criada_em"]

