import uuid
from datetime import timedelta
from django.db import models


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


class Missao(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    titulo = models.CharField(max_length=160)
    objetivo = models.TextField()
    criterio_conclusao = models.TextField()
    resultado_esperado = models.TextField(blank=True)
    origem = models.CharField(max_length=24, choices=OrigemMissao.choices)
    estado = models.CharField(max_length=24, choices=EstadoMissao.choices)
    criador = models.ForeignKey("catalogo.OperadorGestor", related_name="missoes_criadas", on_delete=models.PROTECT)
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
