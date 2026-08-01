import uuid

from django.core.exceptions import ValidationError
from django.db import models


class ResultadoEvento(models.TextChoices):
    CONCLUIDO = "CONCLUIDO", "Concluído"
    REJEITADO = "REJEITADO", "Rejeitado"
    PENDENTE = "PENDENTE", "Pendente"
    FALHA = "FALHA", "Falha"


class EventoOperacional(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tipo = models.CharField(max_length=120)
    versao_esquema = models.PositiveSmallIntegerField(default=1)
    ocorrido_em = models.DateTimeField()
    registrado_em = models.DateTimeField(auto_now_add=True)
    operador = models.ForeignKey(
        "catalogo.OperadorGestor",
        related_name="eventos_operacionais",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
    )
    origem = models.CharField(max_length=80)
    origem_offline = models.BooleanField(default=False)
    alvo_tipo = models.CharField(max_length=80)
    alvo_id = models.CharField(max_length=80)
    acao = models.CharField(max_length=120)
    valores_anteriores = models.JSONField(default=dict)
    valores_posteriores = models.JSONField(default=dict)
    correlacao_id = models.UUIDField(default=uuid.uuid4)
    chave_idempotencia = models.CharField(max_length=180, null=True, blank=True, unique=True)
    resultado = models.CharField(
        max_length=24,
        choices=ResultadoEvento.choices,
        default=ResultadoEvento.CONCLUIDO,
    )
    metadados = models.JSONField(default=dict)

    class Meta:
        ordering = ["-ocorrido_em", "-registrado_em"]
        indexes = [
            models.Index(fields=["alvo_tipo", "alvo_id", "ocorrido_em"]),
            models.Index(fields=["tipo", "ocorrido_em"]),
            models.Index(fields=["correlacao_id"]),
        ]

    def save(self, *args, **kwargs):
        if self.pk and type(self).objects.filter(pk=self.pk).exists():
            raise ValidationError("Eventos operacionais são imutáveis.")
        return super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        raise ValidationError("Eventos operacionais não podem ser excluídos.")
