from django.db import models


class EstadoTarefaCognitiva(models.TextChoices):
    PENDENTE = "PENDENTE", "Pendente"
    PROCESSANDO = "PROCESSANDO", "Processando"
    CONCLUIDA = "CONCLUIDA", "Concluída"
    FALHOU = "FALHOU", "Falhou"
    CANCELADA = "CANCELADA", "Cancelada"


class EstadoIntervencaoIA(models.TextChoices):
    GERADA = "GERADA", "Gerada"
    EXIBIDA = "EXIBIDA", "Exibida"
    ACEITA = "ACEITA", "Aceita"
    RECUSADA = "RECUSADA", "Recusada"
    IGNORADA = "IGNORADA", "Ignorada"
    RESOLVIDA = "RESOLVIDA", "Resolvida"


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
    workload = models.CharField(max_length=32, default="assistant")
    provider = models.CharField(max_length=32, blank=True)
    modelo = models.CharField(max_length=120, blank=True)
    tokens_input = models.PositiveIntegerField(null=True, blank=True)
    tokens_output = models.PositiveIntegerField(null=True, blank=True)
    thinking_tokens = models.PositiveIntegerField(null=True, blank=True)
    duracao_ms = models.PositiveIntegerField(null=True, blank=True)
    custo_estimado = models.DecimalField(max_digits=12, decimal_places=6, null=True, blank=True)

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
    ultima_avaliacao_em = models.DateTimeField(null=True, blank=True)
    fingerprint = models.CharField(max_length=64, blank=True)
    severidade = models.CharField(max_length=16, default="NORMAL")
    resolvida_em = models.DateTimeField(null=True, blank=True)
    resolvida_por = models.ForeignKey(
        "catalogo.OperadorGestor",
        related_name="alertas_cognitivos_resolvidos",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
    )

    class Meta:
        constraints = [models.UniqueConstraint(fields=["operador", "chave"], name="cognicao_alerta_operador_chave_uniq")]
        indexes = [models.Index(fields=["operador", "ativa"], name="cognicao_al_operado_8b2b1f_idx")]


class EventoAtividadeCognitiva(models.Model):
    """Telemetria semântica mínima para contextualizar assistência operacional."""

    operador = models.ForeignKey("catalogo.OperadorGestor", on_delete=models.PROTECT)
    tipo = models.CharField(max_length=48)
    alvo_tipo = models.CharField(max_length=48, blank=True)
    alvo_id = models.CharField(max_length=80, blank=True)
    dados = models.JSONField(default=dict, blank=True)
    ocorreu_em = models.DateTimeField()

    class Meta:
        ordering = ["-ocorreu_em", "-id"]
        indexes = [
            models.Index(fields=["operador", "ocorreu_em"]),
            models.Index(fields=["operador", "alvo_tipo", "alvo_id", "ocorreu_em"]),
        ]


class IntervencaoIA(models.Model):
    operador = models.ForeignKey("catalogo.OperadorGestor", on_delete=models.PROTECT)
    tarefa = models.OneToOneField(
        TarefaCognitiva,
        related_name="intervencao",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
    )
    alerta_principal = models.ForeignKey(
        AlertaCognitiva,
        related_name="intervencoes",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
    )
    alertas = models.JSONField(default=list, blank=True)
    provider = models.CharField(max_length=32, default="gemini")
    modelo = models.CharField(max_length=120, blank=True)
    estrategia = models.CharField(max_length=48, default="intervention")
    mensagem = models.TextField()
    acoes_disponiveis = models.JSONField(default=list, blank=True)
    contexto_hash = models.CharField(max_length=64, blank=True)
    estado = models.CharField(max_length=16, choices=EstadoIntervencaoIA.choices, default=EstadoIntervencaoIA.GERADA)
    criada_em = models.DateTimeField(auto_now_add=True)
    exibida_em = models.DateTimeField(null=True, blank=True)
    resposta_usuario = models.CharField(max_length=24, blank=True)
    respondida_em = models.DateTimeField(null=True, blank=True)
    resultado = models.JSONField(default=dict, blank=True)
    tokens_input = models.PositiveIntegerField(null=True, blank=True)
    tokens_output = models.PositiveIntegerField(null=True, blank=True)
    thinking_tokens = models.PositiveIntegerField(null=True, blank=True)
    duracao_ms = models.PositiveIntegerField(null=True, blank=True)
    custo_estimado = models.DecimalField(max_digits=12, decimal_places=6, null=True, blank=True)

    class Meta:
        ordering = ["-criada_em", "-id"]
        indexes = [
            models.Index(fields=["operador", "estado", "criada_em"]),
            models.Index(fields=["contexto_hash"]),
        ]
