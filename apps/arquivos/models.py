import uuid
from pathlib import Path

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db import models
from django.utils.deconstruct import deconstructible


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


class EstadoPreparacaoArte(models.TextChoices):
    NAO_INICIADA = "NAO_INICIADA", "Arte nao iniciada"
    EM_PREPARACAO = "EM_PREPARACAO", "Arte em preparacao"
    CONCLUIDA = "CONCLUIDA", "Arte concluida"


class PreparacaoArtePedido(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    pedido = models.OneToOneField(
        "pedidos.Pedido", related_name="preparacao_arte", on_delete=models.PROTECT
    )
    estado = models.CharField(
        max_length=24,
        choices=EstadoPreparacaoArte.choices,
        default=EstadoPreparacaoArte.NAO_INICIADA,
    )
    responsavel = models.ForeignKey(
        "catalogo.OperadorGestor",
        related_name="preparacoes_arte_responsavel",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
    )
    iniciado_em = models.DateTimeField(null=True, blank=True)
    ultima_atividade_em = models.DateTimeField(null=True, blank=True)
    proximo_alerta_em = models.DateTimeField(null=True, blank=True)
    adiado_para_data = models.DateField(null=True, blank=True)
    alertas_inatividade_respondidos = models.PositiveIntegerField(default=0)
    ajuda_urgente_solicitada_em = models.DateTimeField(null=True, blank=True)
    concluido_em = models.DateTimeField(null=True, blank=True)
    concluido_por = models.ForeignKey(
        "catalogo.OperadorGestor",
        related_name="preparacoes_arte_concluidas",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
    )
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-atualizado_em"]


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
    modificado_em_ns = models.PositiveBigIntegerField(null=True, blank=True)
    modificacao_detectada_em = models.DateTimeField(null=True, blank=True)
    alteracao_pos_conclusao_pendente = models.BooleanField(default=False)
    ultima_modificacao_por = models.ForeignKey(
        "catalogo.OperadorGestor",
        related_name="arquivos_oficiais_modificados",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
    )
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
    encerrado_em = models.DateTimeField(null=True, blank=True)
    encerrado_por = models.ForeignKey(
        "catalogo.OperadorGestor",
        related_name="vinculos_arquivo_oficial_encerrados",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
    )
    encerramento_observacao = models.TextField(blank=True)
    backup_previo_confirmado = models.BooleanField(default=False)
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


def anexo_upload_to(instance, filename):
    return f"pedidos/{instance.pedido_id}/{instance.id}/{filename}"


@deconstructible
class ArmazenamentoAnexos(FileSystemStorage):
    def __init__(self):
        super().__init__(
            location=Path(settings.DATA_DIR) / "anexos_privados",
            base_url=None,
        )

    def url(self, name):
        raise ValueError("Anexos privados nao possuem URL publica.")


class AnexoPedido(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    pedido = models.ForeignKey(
        "pedidos.Pedido", related_name="anexos", on_delete=models.PROTECT
    )
    arquivo = models.FileField(
        upload_to=anexo_upload_to,
        storage=ArmazenamentoAnexos(),
    )
    nome_original = models.CharField(max_length=255)
    tamanho_bytes = models.PositiveBigIntegerField(default=0)
    conteudo_sha256 = models.CharField(max_length=64)
    criado_por = models.ForeignKey(
        "catalogo.OperadorGestor",
        related_name="anexos_pedido_adicionados",
        on_delete=models.PROTECT,
    )
    criado_em = models.DateTimeField(auto_now_add=True)
    desvinculado_por = models.ForeignKey(
        "catalogo.OperadorGestor",
        related_name="anexos_pedido_desvinculados",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
    )
    desvinculado_em = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["criado_em", "nome_original"]
        indexes = [
            models.Index(fields=["pedido", "desvinculado_em"]),
            models.Index(fields=["pedido", "conteudo_sha256"]),
        ]

    def delete(self, *args, **kwargs):
        raise ValueError("O anexo deve ser desvinculado, nunca apagado.")
