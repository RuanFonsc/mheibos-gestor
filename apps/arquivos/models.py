import uuid

from django.db import models


class OrigemArquivoOficial(models.TextChoices):
    CRIADO_MHEIBOS = "CRIADO_MHEIBOS", "Criado pelo Mheibos"
    VINCULADO_MANUAL = "VINCULADO_MANUAL", "Vinculado manualmente"
    LEGADO = "LEGADO", "Compatibilidade legada"


class EstadoIntegridadeArquivo(models.TextChoices):
    NAO_VERIFICADO = "NAO_VERIFICADO", "Nao verificado"
    INTEGRO = "INTEGRO", "Integro"
    ALERTA = "ALERTA", "Alerta de integridade"


class EstadoVinculoArquivo(models.TextChoices):
    ATIVO = "ATIVO", "Ativo"
    ENCERRADO = "ENCERRADO", "Encerrado"


class ArquivoOficialArte(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    pedido = models.ForeignKey(
        "pedidos.Pedido", related_name="arquivos_oficiais_arte", on_delete=models.PROTECT
    )
    caminho_oficial = models.CharField(max_length=1000)
    nome_oficial = models.CharField(max_length=255)
    extensao = models.CharField(max_length=32, blank=True)
    origem = models.CharField(max_length=24, choices=OrigemArquivoOficial.choices)
    estado_integridade = models.CharField(
        max_length=24,
        choices=EstadoIntegridadeArquivo.choices,
        default=EstadoIntegridadeArquivo.NAO_VERIFICADO,
    )
    estado_vinculo = models.CharField(
        max_length=16,
        choices=EstadoVinculoArquivo.choices,
        default=EstadoVinculoArquivo.ATIVO,
    )
    tamanho_bytes = models.PositiveBigIntegerField(null=True, blank=True)
    largura_px = models.PositiveIntegerField(null=True, blank=True)
    altura_px = models.PositiveIntegerField(null=True, blank=True)
    resolucao_dpi = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    propriedades_tecnicas = models.JSONField(default=dict, blank=True)
    discrepancias = models.JSONField(default=list, blank=True)
    verificado_em = models.DateTimeField(null=True, blank=True)
    alerta_reconhecido_em = models.DateTimeField(null=True, blank=True)
    alerta_reconhecido_por = models.ForeignKey(
        "catalogo.OperadorGestor",
        related_name="alertas_arquivo_reconhecidos",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
    )
    criado_por = models.ForeignKey(
        "catalogo.OperadorGestor",
        related_name="arquivos_oficiais_criados",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
    )
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["criado_em", "nome_oficial"]
        indexes = [
            models.Index(fields=["pedido", "estado_vinculo"]),
            models.Index(fields=["nome_oficial"]),
            models.Index(fields=["estado_integridade"]),
        ]

    def save(self, *args, **kwargs):
        if self.pk:
            anterior = type(self).objects.filter(pk=self.pk).values(
                "pedido_id", "caminho_oficial", "nome_oficial"
            ).first()
            if anterior and (
                anterior["pedido_id"] != self.pedido_id
                or anterior["caminho_oficial"] != self.caminho_oficial
                or anterior["nome_oficial"] != self.nome_oficial
            ):
                raise ValueError("A identidade fisica do arquivo oficial e imutavel.")
        return super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        raise ValueError("O vinculo oficial deve ser encerrado, nunca apagado.")
