from django.urls import path

from .views import assistente, interface_inventario, confirmar_alteracao_status, enviar_mensagem, notificacoes_alertas, registrar_atividade_view, responder_intervencao, resumo_pedido, tarefa_status, whatsapp, whatsapp_etiqueta


urlpatterns = [
    path("assistente/", assistente, name="cognicao_assistente"),
    path("whatsapp/", whatsapp, name="whatsapp_home"),
    path("whatsapp/etiquetas/", whatsapp_etiqueta, name="whatsapp_etiqueta"),
    path("assistente/inventario/", interface_inventario, name="cognicao_interface_inventario"),
    path("assistente/mensagens/", enviar_mensagem, name="cognicao_enviar_mensagem"),
    path("assistente/tarefas/<int:pk>/", tarefa_status, name="cognicao_tarefa_status"),
    path("assistente/notificacoes-alertas/", notificacoes_alertas, name="cognicao_notificacoes_alertas"),
    path("assistente/intervencoes/<int:pk>/resposta/", responder_intervencao, name="cognicao_responder_intervencao"),
    path("assistente/acoes/alterar-status/", confirmar_alteracao_status, name="cognicao_confirmar_status"),
    path("atividade/", registrar_atividade_view, name="cognicao_registrar_atividade"),
    path("pedidos/<int:pk>/resumo/", resumo_pedido, name="cognicao_resumo_pedido")
]
