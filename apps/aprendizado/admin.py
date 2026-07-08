from django.contrib import admin

from apps.aprendizado.models import AmostraTreinamento, ConversaAprendizado, MensagemAprendizado


@admin.register(ConversaAprendizado)
class ConversaAprendizadoAdmin(admin.ModelAdmin):
    list_display = ("nome_contato", "telefone", "instancia", "total_mensagens", "tem_lead", "tem_reclamacao", "util_para_treinamento", "ultima_mensagem_em")
    list_filter = ("origem", "instancia", "tem_lead", "tem_reclamacao", "tem_sinal_pedido", "util_para_treinamento")
    search_fields = ("nome_contato", "telefone", "contato_id")


@admin.register(MensagemAprendizado)
class MensagemAprendizadoAdmin(admin.ModelAdmin):
    list_display = ("conversa", "direcao", "tipo", "enviada_em")
    list_filter = ("direcao", "tipo")
    search_fields = ("texto", "mensagem_id", "conversa__nome_contato", "conversa__telefone")


@admin.register(AmostraTreinamento)
class AmostraTreinamentoAdmin(admin.ModelAdmin):
    list_display = ("conversa", "tipo", "qualidade", "pronta", "criada_em")
    list_filter = ("tipo", "pronta", "qualidade")
