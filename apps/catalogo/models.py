from django.db import models


class CategoriaProduto(models.TextChoices):
    PAINEL = "PAINEL", "Painel"
    BOLSA = "BOLSA", "Bolsa"
    GRAFICA_RAPIDA = "GRAFICA_RAPIDA", "Grafica rapida"
    COMUNICACAO_VISUAL = "COMUNICACAO_VISUAL", "Comunicacao visual"
    OUTROS = "OUTROS", "Outros"


class UnidadeMedida(models.TextChoices):
    UNIDADE = "UN", "Unidade"
    METRO = "M", "Metro"
    METRO_QUADRADO = "M2", "Metro quadrado"
    FOLHA = "FOLHA", "Folha"
    SERVICO = "SERVICO", "Servico"


class CategoriaServico(models.Model):
    nome = models.CharField(max_length=80, unique=True)
    ativa = models.BooleanField(default=True)
    ordem = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["ordem", "nome"]

    def __str__(self):
        return self.nome


class ProdutoServico(models.Model):
    nome = models.CharField(max_length=180, unique=True)
    categoria_servico = models.ForeignKey(
        CategoriaServico,
        related_name="produtos",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
    )
    categoria = models.CharField(
        max_length=32,
        choices=CategoriaProduto.choices,
        default=CategoriaProduto.OUTROS,
    )
    unidade = models.CharField(
        max_length=16,
        choices=UnidadeMedida.choices,
        default=UnidadeMedida.UNIDADE,
    )
    preco_venda_padrao = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    custo_estimado = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    ativo = models.BooleanField(default=True)
    origem_legado = models.CharField(max_length=80, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["nome"]
        indexes = [
            models.Index(fields=["categoria", "ativo"]),
            models.Index(fields=["nome"]),
        ]

    def __str__(self):
        return self.nome


class PreferenciaUI(models.Model):
    chave = models.CharField(max_length=64, unique=True, default="global")
    dados = models.JSONField(default=dict, blank=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Preferência de interface"
        verbose_name_plural = "Preferências de interface"

    def __str__(self):
        return self.chave


class OperadorGestor(models.Model):
    nome = models.CharField(max_length=80, unique=True)
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["nome"]

    def __str__(self):
        return self.nome
