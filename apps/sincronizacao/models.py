import uuid

from django.contrib.auth.hashers import check_password
from django.db import models


class EstadoUnidade(models.TextChoices):
    AGUARDANDO = "AGUARDANDO", "Aguardando envio"
    PREPARANDO = "PREPARANDO", "Preparando"
    ENVIANDO = "ENVIANDO", "Enviando"
    RECEBIDA = "RECEBIDA", "Recebida pela Central"
    INCORPORADA = "INCORPORADA", "Incorporada"
    FALHA_TEMPORARIA = "FALHA_TEMPORARIA", "Falha temporaria"
    REQUER_ATENCAO = "REQUER_ATENCAO", "Requer atencao"


class EstacaoCliente(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome = models.CharField(max_length=120, unique=True)
    segredo_hash = models.CharField(max_length=128)
    ativa = models.BooleanField(default=True)
    criada_em = models.DateTimeField(auto_now_add=True)
    atualizada_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["nome"]

    def verifica_segredo(self, segredo: str) -> bool:
        return self.ativa and check_password(segredo, self.segredo_hash)


class SequenciaOffline(models.Model):
    estacao_id = models.UUIDField()
    codigo_origem = models.CharField(max_length=12)
    ultimo_numero = models.PositiveBigIntegerField(default=0)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["estacao_id", "codigo_origem"],
                name="uniq_sequencia_offline_estacao_origem",
            )
        ]


class UnidadeSincronizacao(models.Model):
    CAMPOS_IMUTAVEIS = (
        "chave_idempotencia",
        "entidade_local_id",
        "pedido_local_id",
        "estacao_id",
        "operador_id",
        "codigo_visivel",
        "sequencia_local",
        "versao_esquema",
        "versao_politica",
        "payload",
        "checksum",
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    chave_idempotencia = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    entidade_local_id = models.UUIDField(unique=True)
    pedido_local = models.OneToOneField(
        "pedidos.Pedido", related_name="unidade_sincronizacao", on_delete=models.PROTECT
    )
    estacao_id = models.UUIDField()
    operador = models.ForeignKey("catalogo.OperadorGestor", on_delete=models.PROTECT)
    codigo_visivel = models.CharField(max_length=40)
    sequencia_local = models.PositiveBigIntegerField()
    versao_esquema = models.PositiveSmallIntegerField(default=1)
    versao_politica = models.CharField(max_length=80)
    payload = models.JSONField()
    checksum = models.CharField(max_length=64)
    estado = models.CharField(
        max_length=32, choices=EstadoUnidade.choices, default=EstadoUnidade.AGUARDANDO
    )
    tentativas = models.PositiveIntegerField(default=0)
    ultima_tentativa_em = models.DateTimeField(null=True, blank=True)
    proxima_tentativa_em = models.DateTimeField(null=True, blank=True)
    ultimo_resultado = models.CharField(max_length=120, blank=True)
    motivo_falha = models.TextField(blank=True)
    pedido_global_id_confirmado = models.PositiveBigIntegerField(null=True, blank=True)
    codigo_confirmacao = models.CharField(max_length=32, blank=True)
    incorporada_em = models.DateTimeField(null=True, blank=True)
    criada_em = models.DateTimeField(auto_now_add=True)
    atualizada_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["criada_em"]
        indexes = [
            models.Index(fields=["estado", "criada_em"]),
            models.Index(fields=["estacao_id", "sequencia_local"]),
        ]

    def save(self, *args, **kwargs):
        if self.pk:
            anterior = type(self).objects.filter(pk=self.pk).values(
                *self.CAMPOS_IMUTAVEIS
            ).first()
            if anterior and any(
                anterior[campo] != getattr(self, campo) for campo in self.CAMPOS_IMUTAVEIS
            ):
                raise ValueError("Conteudo causal da unidade de sincronizacao e imutavel.")
        return super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        raise ValueError("Unidades de sincronizacao nao podem ser descartadas.")


class IncorporacaoOffline(models.Model):
    chave_idempotencia = models.UUIDField(unique=True)
    entidade_local_id = models.UUIDField(unique=True)
    estacao_id = models.UUIDField()
    codigo_visivel = models.CharField(max_length=40, unique=True)
    pedido_global = models.OneToOneField(
        "pedidos.Pedido", related_name="incorporacao_offline", on_delete=models.PROTECT
    )
    checksum = models.CharField(max_length=64)
    incorporada_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-incorporada_em"]
