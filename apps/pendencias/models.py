import uuid

from django.db import models
from django.db.models import Q


class EstadoPendencia(models.TextChoices):
    ABERTA = "ABERTA", "Aberta"
    ENCERRADA = "ENCERRADA", "Encerrada"


class FormaEncerramentoPendencia(models.TextChoices):
    RESOLUCAO = "RESOLUCAO", "Resolucao"
    CANCELAMENTO_AUTORIZADO = "CANCELAMENTO_AUTORIZADO", "Cancelamento autorizado"
    INCORPORACAO_PROCESSO = "INCORPORACAO_PROCESSO", "Incorporacao a outro processo"


class Pendencia(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tipo = models.CharField(max_length=80)
    descricao = models.TextField()
    processo = models.ForeignKey(
        "operacao.Processo", related_name="pendencias", on_delete=models.PROTECT
    )
    pedido = models.ForeignKey(
        "pedidos.Pedido", related_name="pendencias", on_delete=models.PROTECT
    )
    responsavel_principal = models.ForeignKey(
        "catalogo.OperadorGestor",
        related_name="pendencias_responsaveis",
        on_delete=models.PROTECT,
    )
    destinatarios = models.ManyToManyField(
        "catalogo.OperadorGestor", related_name="pendencias_destinatarias", blank=True
    )
    prazo = models.DateTimeField(null=True, blank=True)
    prioridade = models.CharField(max_length=24, blank=True)
    criticidade = models.CharField(max_length=24, blank=True)
    estado = models.CharField(
        max_length=16, choices=EstadoPendencia.choices, default=EstadoPendencia.ABERTA
    )
    forma_encerramento = models.CharField(
        max_length=40, choices=FormaEncerramentoPendencia.choices, blank=True
    )
    encerrada_por = models.ForeignKey(
        "catalogo.OperadorGestor",
        related_name="pendencias_encerradas",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
    )
    criada_em = models.DateTimeField(auto_now_add=True)
    encerrada_em = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-criada_em"]
        constraints = [
            models.UniqueConstraint(
                fields=["processo", "tipo"],
                condition=Q(encerrada_em__isnull=True),
                name="pendencia_aberta_tipo_processo_unica",
            )
        ]
