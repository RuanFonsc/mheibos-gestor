from django.db import models


class TipoEvidencia(models.TextChoices):
    FATO = "FATO", "Fato"
    CORRELACAO = "CORRELACAO", "Correlação"
    INFERENCIA = "INFERENCIA", "Inferência"
    HIPOTESE = "HIPOTESE", "Hipótese"


class EstadoAnalise(models.TextChoices):
    RASCUNHO = "RASCUNHO", "Rascunho"
    VALIDADA = "VALIDADA", "Validada"
    ARQUIVADA = "ARQUIVADA", "Arquivada"


class EstadoSimulacao(models.TextChoices):
    SALVA = "SALVA", "Salva"
    EXPIRADA = "EXPIRADA", "Expirada"
    PROMOVIDA = "PROMOVIDA", "Promovida para missão"
    ARQUIVADA = "ARQUIVADA", "Arquivada"


class EvidenciaAnalitica(models.Model):
    titulo = models.CharField(max_length=180)
    descricao = models.TextField()
    tipo = models.CharField(max_length=16, choices=TipoEvidencia.choices)
    fonte = models.CharField(max_length=240)
    referencia = models.CharField(max_length=180, blank=True)
    dados = models.JSONField(default=dict, blank=True)
    confianca = models.PositiveSmallIntegerField(default=100)
    coletada_em = models.DateTimeField()
    autor = models.ForeignKey("catalogo.OperadorGestor", null=True, blank=True, on_delete=models.PROTECT, related_name="evidencias_analiticas")
    criada_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-coletada_em", "-id"]
        indexes = [models.Index(fields=["tipo", "coletada_em"])]

    def __str__(self):
        return self.titulo


class Analise(models.Model):
    pergunta = models.CharField(max_length=240)
    resumo = models.TextField()
    estado = models.CharField(max_length=16, choices=EstadoAnalise.choices, default=EstadoAnalise.RASCUNHO)
    confianca = models.PositiveSmallIntegerField(default=0)
    autor = models.ForeignKey("catalogo.OperadorGestor", on_delete=models.PROTECT, related_name="analises_criadas")
    evidencias = models.ManyToManyField(EvidenciaAnalitica, related_name="analises", blank=True)
    criada_em = models.DateTimeField(auto_now_add=True)
    atualizada_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-atualizada_em", "-id"]

    def __str__(self):
        return self.pergunta


class Simulacao(models.Model):
    titulo = models.CharField(max_length=180)
    objetivo = models.TextField()
    premissas = models.JSONField(default=dict)
    resultado = models.JSONField(default=dict)
    estado = models.CharField(max_length=16, choices=EstadoSimulacao.choices, default=EstadoSimulacao.SALVA)
    validade_ate = models.DateTimeField(null=True, blank=True)
    autor = models.ForeignKey("catalogo.OperadorGestor", on_delete=models.PROTECT, related_name="simulacoes_criadas")
    missao = models.OneToOneField("missoes.Missao", null=True, blank=True, on_delete=models.PROTECT, related_name="simulacao_origem")
    criada_em = models.DateTimeField(auto_now_add=True)
    atualizada_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-atualizada_em", "-id"]
        indexes = [models.Index(fields=["estado", "validade_ate"])]

    def __str__(self):
        return self.titulo
