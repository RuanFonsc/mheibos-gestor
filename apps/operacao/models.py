import uuid

from django.core.exceptions import ValidationError
from django.db import models


class EstadoProcesso(models.TextChoices):
    NAO_INICIADO = "NAO_INICIADO", "Nao iniciado"
    EM_ANDAMENTO = "EM_ANDAMENTO", "Em andamento"
    BLOQUEADO = "BLOQUEADO", "Bloqueado"
    CONCLUIDO = "CONCLUIDO", "Concluido"
    CANCELADO = "CANCELADO", "Cancelado"
    INVIABILIZADO = "INVIABILIZADO", "Inviabilizado"
    ABANDONADO = "ABANDONADO", "Abandonado"
    SUBSTITUIDO = "SUBSTITUIDO", "Substituido"


class EstadoEtapa(models.TextChoices):
    NAO_INICIADA = "NAO_INICIADA", "Nao iniciada"
    AGUARDANDO_CONDICAO = "AGUARDANDO_CONDICAO", "Aguardando condicao externa"
    PRONTA = "PRONTA", "Pronta para execucao"
    EM_ANDAMENTO = "EM_ANDAMENTO", "Em andamento"
    BLOQUEADA = "BLOQUEADA", "Bloqueada"
    CONCLUIDA = "CONCLUIDA", "Concluida"
    DISPENSADA = "DISPENSADA", "Dispensada"
    CANCELADA = "CANCELADA", "Cancelada"
    REABERTA = "REABERTA", "Reaberta"


class ModeloFluxo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    codigo = models.CharField(max_length=80)
    nome = models.CharField(max_length=160)
    versao = models.PositiveIntegerField()
    definicao_etapas = models.JSONField(default=list)
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["codigo", "versao"], name="operacao_fluxo_versao_unica")]

    def save(self, *args, **kwargs):
        if self.pk and Processo.objects.filter(modelo_fluxo_id=self.pk).exists():
            raise ValidationError("Uma versao de fluxo instanciada e imutavel.")
        return super().save(*args, **kwargs)


class Processo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tipo = models.CharField(max_length=80)
    objetivo = models.TextField()
    resultado_esperado = models.TextField()
    pedido = models.ForeignKey("pedidos.Pedido", related_name="processos", on_delete=models.PROTECT)
    modelo_fluxo = models.ForeignKey(ModeloFluxo, on_delete=models.PROTECT)
    modelo_codigo_snapshot = models.CharField(max_length=80)
    modelo_versao_snapshot = models.PositiveIntegerField()
    estado_operacional = models.CharField(max_length=24, choices=EstadoProcesso.choices, default=EstadoProcesso.NAO_INICIADO)
    confirmado_em = models.DateTimeField(null=True, blank=True)
    iniciado_em = models.DateTimeField(null=True, blank=True)
    concluido_em = models.DateTimeField(null=True, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["pedido", "tipo"], name="operacao_processo_tipo_pedido_unico")]


class EtapaProcesso(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    processo = models.ForeignKey(Processo, related_name="etapas", on_delete=models.PROTECT)
    chave = models.CharField(max_length=80)
    nome = models.CharField(max_length=160)
    descricao = models.TextField(blank=True)
    ordem = models.PositiveIntegerField()
    obrigatoria = models.BooleanField(default=True)
    estado = models.CharField(max_length=24, choices=EstadoEtapa.choices)
    responsavel = models.ForeignKey("catalogo.OperadorGestor", related_name="etapas_responsaveis", null=True, blank=True, on_delete=models.PROTECT)
    concluida_por = models.ForeignKey("catalogo.OperadorGestor", related_name="etapas_concluidas", null=True, blank=True, on_delete=models.PROTECT)
    motivo_bloqueio = models.TextField(blank=True)
    iniciada_em = models.DateTimeField(null=True, blank=True)
    concluida_em = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["processo_id", "ordem"]
        constraints = [models.UniqueConstraint(fields=["processo", "chave"], name="operacao_etapa_chave_unica")]
