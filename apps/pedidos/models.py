from decimal import Decimal

from django.conf import settings
from django.db import models


class StatusPedido(models.TextChoices):
    EM_ATENDIMENTO = "EM_ATENDIMENTO", "Em atendimento"
    AGUARDANDO_ARTE = "AGUARDANDO_ARTE", "Aguardando arte"
    ARTE_EM_PREPARO = "ARTE_EM_PREPARO", "Arte em preparo"
    AGUARDANDO_APROVACAO = "AGUARDANDO_APROVACAO", "Aguardando aprovacao"
    LIBERADO_PRODUCAO = "LIBERADO_PRODUCAO", "Liberado para producao"
    EM_PRODUCAO = "EM_PRODUCAO", "Em producao"
    PRONTO = "PRONTO", "Pronto para entrega"
    ENTREGUE = "ENTREGUE", "Entregue"
    CANCELADO = "CANCELADO", "Cancelado"


class PrioridadePedido(models.TextChoices):
    BAIXA = "BAIXA", "Baixa"
    NORMAL = "NORMAL", "Normal"
    ALTA = "ALTA", "Alta"
    URGENTE = "URGENTE", "Urgente"


STATUS_PRE_PRODUCAO = [
    StatusPedido.EM_ATENDIMENTO,
    StatusPedido.AGUARDANDO_ARTE,
    StatusPedido.ARTE_EM_PREPARO,
    StatusPedido.AGUARDANDO_APROVACAO,
]

STATUS_PRODUCAO = [
    StatusPedido.LIBERADO_PRODUCAO,
    StatusPedido.EM_PRODUCAO,
]

STATUS_ASSISTENCIA = STATUS_PRE_PRODUCAO
STATUS_FUNIL_GESTOR = STATUS_PRE_PRODUCAO + STATUS_PRODUCAO

STATUS_ENTREGA = [
    StatusPedido.PRONTO,
]


class FormaPagamento(models.TextChoices):
    PIX = "PIX", "PIX"
    DINHEIRO = "DINHEIRO", "Dinheiro"
    CARTAO = "CARTAO", "Cartao"
    CHEQUE = "CHEQUE", "Cheque"
    TRANSFERENCIA = "TRANSFERENCIA", "Transferencia"
    OUTRO = "OUTRO", "Outro"
    NAO_INFORMADO = "NAO_INFORMADO", "Nao informado"


class OrigemPedido(models.TextChoices):
    BALCAO = "BALCAO", "Balcao"
    WHATSAPP = "WHATSAPP", "WhatsApp"
    IA = "IA", "IA"
    LEGADO = "LEGADO", "Legado"
    OUTRO = "OUTRO", "Outro"


class Pedido(models.Model):
    legado_id = models.PositiveIntegerField(null=True, blank=True, unique=True)
    cliente = models.ForeignKey(
        "clientes.Cliente",
        related_name="pedidos",
        on_delete=models.PROTECT,
    )
    designer = models.CharField(max_length=120, blank=True)
    tema = models.CharField(max_length=180, blank=True)
    descricao_legada = models.TextField(blank=True)
    data_registro = models.DateTimeField(null=True, blank=True)
    data_pedido = models.DateField(null=True, blank=True)
    data_entrega = models.DateField(null=True, blank=True)
    hora_entrega = models.TimeField(null=True, blank=True)
    observacoes = models.TextField(blank=True)
    caminho_arquivo_corel = models.CharField(max_length=500, blank=True)
    valor_total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    valor_pago_legado = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    desconto_ajuste = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    forma_pagamento_legada = models.CharField(
        max_length=32,
        choices=FormaPagamento.choices,
        default=FormaPagamento.NAO_INFORMADO,
    )
    prioridade = models.CharField(
        max_length=16,
        choices=PrioridadePedido.choices,
        default=PrioridadePedido.NORMAL,
    )
    status = models.CharField(
        max_length=32,
        choices=StatusPedido.choices,
        default=StatusPedido.AGUARDANDO_ARTE,
    )
    origem = models.CharField(
        max_length=24,
        choices=OrigemPedido.choices,
        default=OrigemPedido.LEGADO,
    )
    pdf_gerado_por = models.CharField(max_length=120, blank=True)
    usuario_cadastro = models.CharField(max_length=80, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-id"]
        indexes = [
            models.Index(fields=["status", "data_entrega"]),
            models.Index(fields=["prioridade", "data_entrega"]),
            models.Index(fields=["data_pedido"]),
            models.Index(fields=["designer"]),
            models.Index(fields=["origem"]),
        ]

    @property
    def saldo_aberto(self):
        return max(Decimal("0.00"), self.valor_total - self.total_pago)

    @property
    def total_pago(self):
        pagamentos_prefetch = getattr(self, "_prefetched_objects_cache", {}).get("pagamentos")
        if pagamentos_prefetch is not None:
            total = sum(
                (pagamento.valor or Decimal("0.00"))
                for pagamento in pagamentos_prefetch
                if pagamento.status == StatusPagamento.CONFIRMADO
            )
            return max(total, self.valor_pago_legado or Decimal("0.00"))
        total = self.pagamentos.filter(status=StatusPagamento.CONFIRMADO).aggregate(
            soma=models.Sum("valor")
        )["soma"]
        total = total or Decimal("0.00")
        return max(total, self.valor_pago_legado or Decimal("0.00"))

    def status_assistencia(self):
        from apps.catalogo.assistencia import categorias_do_pedido, pedido_entrou_na_regra, regra_categoria, dias_uteis_restantes
        from django.utils import timezone

        if self.status not in STATUS_ASSISTENCIA:
            return {"na_assistencia": False, "mensagem": "Fora da assistência de envio"}
        
        agora = timezone.localtime()
        categorias = categorias_do_pedido(self)
        
        if not categorias:
            return {"na_assistencia": False, "mensagem": "Sem categoria definida"}
            
        # Verifica se entrou na regra para qualquer uma das categorias do pedido
        na_assistencia = any(pedido_entrou_na_regra(self, cat, agora) for cat in categorias)
        
        if na_assistencia:
            return {"na_assistencia": True, "mensagem": "Está na assistência de envio"}
            
        # Se não está, calcula quanto tempo falta (menor limite entre as categorias)
        prazos = []
        for cat in categorias:
            regra = regra_categoria(cat)
            limite = regra["limite_dias_uteis"]
            if limite is not None:
                dias_uteis = dias_uteis_restantes(self.data_entrega, agora.date())
                falta = dias_uteis - limite
                if falta > 0:
                    prazos.append(falta)
        
        if prazos:
            min_falta = min(prazos)
            sufixo = "dia" if min_falta == 1 else "dias"
            return {"na_assistencia": False, "mensagem": f"Faltam {min_falta} {sufixo} úteis para entrar"}
            
        return {"na_assistencia": False, "mensagem": "Não entra na assistência"}

    def __str__(self):
        return f"Pedido #{self.pk} - {self.cliente}"


class PedidoItem(models.Model):
    pedido = models.ForeignKey(Pedido, related_name="itens", on_delete=models.CASCADE)
    produto = models.ForeignKey(
        "catalogo.ProdutoServico",
        related_name="itens_pedido",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
    )
    categoria_servico = models.ForeignKey(
        "catalogo.CategoriaServico",
        related_name="itens_pedido",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
    )
    nome = models.CharField(max_length=180)
    descricao = models.TextField(blank=True)
    quantidade = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    preco_unitario = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    custo_unitario_estimado = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    ordem = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["pedido_id", "ordem", "id"]
        indexes = [models.Index(fields=["nome"])]

    @property
    def subtotal(self):
        return self.quantidade * self.preco_unitario

    @property
    def custo_total_estimado(self):
        return self.quantidade * self.custo_unitario_estimado

    def __str__(self):
        return f"{self.quantidade}x {self.nome}"


def arte_upload_to(instance, filename):
    pedido_id = instance.pedido_id or "sem-pedido"
    return f"pedidos/{pedido_id}/artes/{filename}"


class ArtePedido(models.Model):
    pedido = models.ForeignKey(Pedido, related_name="artes", on_delete=models.CASCADE)
    arquivo = models.ImageField(upload_to=arte_upload_to)
    nome_original = models.CharField(max_length=255, blank=True)
    tamanho_bytes = models.PositiveBigIntegerField(default=0)
    ordem = models.PositiveIntegerField(default=0)
    legado_base64_hash = models.CharField(max_length=64, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["pedido_id", "ordem", "id"]

    def __str__(self):
        return self.nome_original or self.arquivo.name


class StatusPagamento(models.TextChoices):
    PENDENTE = "PENDENTE", "Pendente"
    CONFIRMADO = "CONFIRMADO", "Confirmado"
    CANCELADO = "CANCELADO", "Cancelado"
    ESTORNADO = "ESTORNADO", "Estornado"


class PagamentoPedido(models.Model):
    pedido = models.ForeignKey(Pedido, related_name="pagamentos", on_delete=models.CASCADE)
    valor = models.DecimalField(max_digits=12, decimal_places=2)
    forma = models.CharField(
        max_length=32,
        choices=FormaPagamento.choices,
        default=FormaPagamento.NAO_INFORMADO,
    )
    data_pagamento = models.DateField(null=True, blank=True)
    status = models.CharField(
        max_length=24,
        choices=StatusPagamento.choices,
        default=StatusPagamento.CONFIRMADO,
    )
    observacoes = models.TextField(blank=True)
    criado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-data_pagamento", "-id"]
        indexes = [
            models.Index(fields=["status", "data_pagamento"]),
            models.Index(fields=["forma"]),
        ]

    def __str__(self):
        return f"{self.pedido} - {self.valor}"


class HistoricoStatusPedido(models.Model):
    pedido = models.ForeignKey(Pedido, related_name="historico_status", on_delete=models.CASCADE)
    status_anterior = models.CharField(max_length=32, choices=StatusPedido.choices, blank=True)
    status_novo = models.CharField(max_length=32, choices=StatusPedido.choices)
    observacao = models.TextField(blank=True)
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-criado_em", "-id"]
