from django.db import models
from django.utils import timezone


class OrigemConversa(models.TextChoices):
    WHATSAPP = "WHATSAPP", "WhatsApp"


class DirecaoMensagem(models.TextChoices):
    CLIENTE = "CLIENTE", "Cliente"
    EMPRESA = "EMPRESA", "Empresa"
    SISTEMA = "SISTEMA", "Sistema"


class TipoAmostraTreinamento(models.TextChoices):
    CONVERSA = "CONVERSA", "Conversa"
    LEAD = "LEAD", "Lead"
    RECLAMACAO = "RECLAMACAO", "Reclamacao"
    PEDIDO = "PEDIDO", "Pedido"


class ConversaAprendizado(models.Model):
    origem = models.CharField(max_length=24, choices=OrigemConversa.choices, default=OrigemConversa.WHATSAPP)
    instancia = models.CharField(max_length=80, blank=True)
    contato_id = models.CharField(max_length=160)
    telefone = models.CharField(max_length=32, blank=True)
    nome_contato = models.CharField(max_length=160, blank=True)
    primeira_mensagem_em = models.DateTimeField(null=True, blank=True)
    ultima_mensagem_em = models.DateTimeField(null=True, blank=True)
    total_mensagens = models.PositiveIntegerField(default=0)
    total_cliente = models.PositiveIntegerField(default=0)
    total_empresa = models.PositiveIntegerField(default=0)
    tem_lead = models.BooleanField(default=False)
    tem_reclamacao = models.BooleanField(default=False)
    tem_sinal_pedido = models.BooleanField(default=False)
    util_para_treinamento = models.BooleanField(default=False)
    revisado = models.BooleanField(default=False)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Conversa de aprendizado"
        verbose_name_plural = "Conversas de aprendizado"
        unique_together = [("origem", "instancia", "contato_id")]
        indexes = [
            models.Index(fields=["origem", "instancia"]),
            models.Index(fields=["ultima_mensagem_em"]),
            models.Index(fields=["util_para_treinamento"]),
            models.Index(fields=["tem_lead", "tem_reclamacao"]),
        ]

    def __str__(self):
        return self.nome_contato or self.telefone or self.contato_id


class MensagemAprendizado(models.Model):
    conversa = models.ForeignKey(ConversaAprendizado, on_delete=models.CASCADE, related_name="mensagens")
    mensagem_id = models.CharField(max_length=160)
    direcao = models.CharField(max_length=16, choices=DirecaoMensagem.choices)
    tipo = models.CharField(max_length=80, blank=True)
    texto = models.TextField(blank=True)
    enviada_em = models.DateTimeField(default=timezone.now)
    payload = models.JSONField(default=dict, blank=True)
    criada_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Mensagem de aprendizado"
        verbose_name_plural = "Mensagens de aprendizado"
        unique_together = [("conversa", "mensagem_id")]
        ordering = ["enviada_em", "id"]
        indexes = [
            models.Index(fields=["direcao", "tipo"]),
            models.Index(fields=["enviada_em"]),
        ]

    def __str__(self):
        return f"{self.conversa} - {self.get_direcao_display()}"


class AmostraTreinamento(models.Model):
    conversa = models.ForeignKey(ConversaAprendizado, on_delete=models.CASCADE, related_name="amostras")
    tipo = models.CharField(max_length=24, choices=TipoAmostraTreinamento.choices)
    conteudo = models.JSONField(default=dict)
    qualidade = models.PositiveSmallIntegerField(default=1)
    pronta = models.BooleanField(default=False)
    criada_em = models.DateTimeField(auto_now_add=True)
    atualizada_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Amostra de treinamento"
        verbose_name_plural = "Amostras de treinamento"
        unique_together = [("conversa", "tipo")]
        indexes = [
            models.Index(fields=["tipo", "pronta"]),
        ]

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.conversa}"


class CamadaConhecimento(models.TextChoices):
    UNIVERSAL = "UNIVERSAL", "Universal do Mheibos"
    INSTITUCIONAL = "INSTITUCIONAL", "Institucional da empresa"
    OPERACIONAL = "OPERACIONAL", "Operacional"
    MEMORIA_LONGA = "MEMORIA_LONGA", "Memória de longo prazo"
    MEMORIA_CURTA = "MEMORIA_CURTA", "Memória de curto prazo"


class EstadoConhecimento(models.TextChoices):
    PENDENTE = "PENDENTE", "Pendente"
    APROVADO = "APROVADO", "Aprovado"
    REJEITADO = "REJEITADO", "Rejeitado"
    ARQUIVADO = "ARQUIVADO", "Arquivado"


class Conhecimento(models.Model):
    titulo = models.CharField(max_length=200)
    conteudo = models.TextField()
    camada = models.CharField(max_length=24, choices=CamadaConhecimento.choices)
    estado = models.CharField(max_length=16, choices=EstadoConhecimento.choices, default=EstadoConhecimento.PENDENTE)
    fonte = models.CharField(max_length=240)
    autor = models.ForeignKey("catalogo.OperadorGestor", null=True, blank=True, on_delete=models.PROTECT)
    versao = models.PositiveIntegerField(default=1)
    valido_de = models.DateTimeField(null=True, blank=True)
    valido_ate = models.DateTimeField(null=True, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-atualizado_em", "-id"]
        indexes = [models.Index(fields=["camada", "estado"]), models.Index(fields=["fonte"])]

    def __str__(self):
        return self.titulo
