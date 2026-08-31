from django.db import models


class EstadoTarefaCognitiva(models.TextChoices):
    PENDENTE = "PENDENTE", "Pendente"
    PROCESSANDO = "PROCESSANDO", "Processando"
    CONCLUIDA = "CONCLUIDA", "Concluída"
    FALHOU = "FALHOU", "Falhou"
    CANCELADA = "CANCELADA", "Cancelada"


class ConversaCognitiva(models.Model):
    operador = models.ForeignKey("catalogo.OperadorGestor", null=True, blank=True, on_delete=models.PROTECT)
    origem = models.CharField(max_length=24, default="GESTOR", choices=[("GESTOR", "Gestor"), ("WHATSAPP", "WhatsApp")])
    referencia_externa = models.CharField(max_length=200, blank=True)
    titulo = models.CharField(max_length=200, blank=True)
    contexto = models.JSONField(default=dict, blank=True)
    ativa = models.BooleanField(default=True)
    criada_em = models.DateTimeField(auto_now_add=True)
    atualizada_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-atualizada_em", "-id"]
        indexes = [models.Index(fields=["operador", "ativa"]), models.Index(fields=["origem", "referencia_externa"])]


class MensagemCognitiva(models.Model):
    conversa = models.ForeignKey(ConversaCognitiva, on_delete=models.CASCADE, related_name="mensagens")
    papel = models.CharField(max_length=16, choices=[("USUARIO", "Usuário"), ("MHEIBOS", "Mheibos"), ("SISTEMA", "Sistema"), ("WHATSAPP", "WhatsApp")])
    texto = models.TextField()
    metadados = models.JSONField(default=dict, blank=True)
    criada_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["criada_em", "id"]


class TarefaCognitiva(models.Model):
    conversa = models.ForeignKey(ConversaCognitiva, on_delete=models.CASCADE, related_name="tarefas")
    mensagem_usuario = models.ForeignKey(MensagemCognitiva, on_delete=models.PROTECT, related_name="tarefas")
    estado = models.CharField(max_length=16, choices=EstadoTarefaCognitiva.choices, default=EstadoTarefaCognitiva.PENDENTE)
    contexto = models.JSONField(default=dict, blank=True)
    resultado = models.JSONField(default=dict, blank=True)
    erro = models.TextField(blank=True)
    criada_em = models.DateTimeField(auto_now_add=True)
    iniciada_em = models.DateTimeField(null=True, blank=True)
    concluida_em = models.DateTimeField(null=True, blank=True)
    notificado_em = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["criada_em", "id"]
        indexes = [models.Index(fields=["estado", "criada_em"])]

class AlertaCognitiva(models.Model):
    operador = models.ForeignKey("catalogo.OperadorGestor", on_delete=models.PROTECT)
    chave = models.CharField(max_length=200)
    dados = models.JSONField(default=dict, blank=True)
    ativa = models.BooleanField(default=True)
    criada_em = models.DateTimeField(auto_now_add=True)
    atualizada_em = models.DateTimeField(auto_now=True)
    ultima_tarefa_em = models.DateTimeField(null=True, blank=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["operador", "chave"], name="cognicao_alerta_operador_chave_uniq")]
        indexes = [models.Index(fields=["operador", "ativa"], name="cognicao_al_operado_8b2b1f_idx")]
