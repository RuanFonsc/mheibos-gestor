from django.db import models


class TipoLancamento(models.TextChoices):
    RECEITA = "RECEITA", "Receita"
    DESPESA = "DESPESA", "Despesa"


class StatusLancamento(models.TextChoices):
    PREVISTO = "PREVISTO", "Previsto"
    REALIZADO = "REALIZADO", "Realizado"
    CANCELADO = "CANCELADO", "Cancelado"


class GrupoFinanceiro(models.TextChoices):
    VENDAS = "VENDAS", "Vendas"
    SERVICOS = "SERVICOS", "Servicos"
    CUSTOS_FIXOS = "CUSTOS_FIXOS", "Custos fixos"
    CUSTOS_VARIAVEIS = "CUSTOS_VARIAVEIS", "Custos variaveis"
    IMPOSTOS = "IMPOSTOS", "Impostos"
    RETIRADAS = "RETIRADAS", "Retiradas"
    OUTROS = "OUTROS", "Outros"


class CategoriaFinanceira(models.Model):
    nome = models.CharField(max_length=120)
    tipo = models.CharField(max_length=16, choices=TipoLancamento.choices)
    grupo = models.CharField(
        max_length=32,
        choices=GrupoFinanceiro.choices,
        default=GrupoFinanceiro.OUTROS,
    )
    ativa = models.BooleanField(default=True)
    ordem = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["tipo", "ordem", "nome"]
        constraints = [
            models.UniqueConstraint(fields=["nome", "tipo"], name="uniq_categoria_tipo")
        ]
        indexes = [models.Index(fields=["tipo", "grupo", "ativa"])]

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.nome}"


class ContaFinanceira(models.Model):
    nome = models.CharField(max_length=120, unique=True)
    descricao = models.TextField(blank=True)
    ativa = models.BooleanField(default=True)

    class Meta:
        ordering = ["nome"]

    def __str__(self):
        return self.nome


class LancamentoFinanceiro(models.Model):
    tipo = models.CharField(max_length=16, choices=TipoLancamento.choices)
    categoria = models.ForeignKey(
        CategoriaFinanceira,
        related_name="lancamentos",
        on_delete=models.PROTECT,
    )
    conta = models.ForeignKey(
        ContaFinanceira,
        related_name="lancamentos",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
    )
    pedido = models.ForeignKey(
        "pedidos.Pedido",
        related_name="lancamentos_financeiros",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
    )
    pagamento_pedido = models.OneToOneField(
        "pedidos.PagamentoPedido",
        related_name="lancamento_financeiro",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
    )
    descricao = models.CharField(max_length=255)
    valor = models.DecimalField(max_digits=12, decimal_places=2)
    data_competencia = models.DateField()
    data_vencimento = models.DateField(null=True, blank=True)
    data_pagamento = models.DateField(null=True, blank=True)
    status = models.CharField(
        max_length=16,
        choices=StatusLancamento.choices,
        default=StatusLancamento.PREVISTO,
    )
    observacoes = models.TextField(blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-data_competencia", "-id"]
        indexes = [
            models.Index(fields=["tipo", "status", "data_competencia"]),
            models.Index(fields=["tipo", "status", "data_pagamento"]),
            models.Index(fields=["categoria", "data_competencia"]),
            models.Index(fields=["pedido"]),
        ]

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.descricao} - {self.valor}"


class MetaVendasUsuario(models.Model):
    operador = models.ForeignKey(
        "catalogo.OperadorGestor",
        related_name="metas_vendas",
        on_delete=models.CASCADE,
    )
    ano = models.PositiveIntegerField()
    mes = models.PositiveSmallIntegerField()
    valor = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-ano", "-mes", "operador__nome"]
        constraints = [
            models.UniqueConstraint(fields=["operador", "ano", "mes"], name="uniq_meta_vendas_operador_mes")
        ]

    def __str__(self):
        return f"{self.operador} - {self.mes:02d}/{self.ano} - {self.valor}"
