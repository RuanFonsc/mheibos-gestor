from django.urls import path

from apps.pedidos import views


urlpatterns = [
    path("", views.pedido_list, name="pedido_list"),
    path("atendimento/", views.atendimento_list, name="atendimento_list"),
    path("novo/", views.pedido_create, name="pedido_create"),
    path("acao-massa/", views.pedido_bulk_action, name="pedido_bulk_action"),
    path("entrega/", views.entrega_list, name="entrega_list"),
    path("<int:pk>/", views.pedido_detail, name="pedido_detail"),
    path("<int:pk>/ordem-servico/", views.pedido_ordem_servico, name="pedido_ordem_servico"),
    path("<int:pk>/editar/", views.pedido_edit, name="pedido_edit"),
    path("<int:pk>/arquivos-oficiais/vincular/", views.pedido_vincular_arquivo_oficial, name="pedido_vincular_arquivo_oficial"),
    path("<int:pk>/arquivos-oficiais/criar/", views.pedido_criar_arquivo_oficial, name="pedido_criar_arquivo_oficial"),
    path("<int:pk>/arte/concluir/", views.pedido_concluir_arte, name="pedido_concluir_arte"),
    path("<int:pk>/arte/responder-inatividade/", views.pedido_responder_alerta_inatividade_arte, name="pedido_responder_alerta_inatividade_arte"),
    path("<int:pk>/arquivos-oficiais/<uuid:arquivo_id>/decidir-alteracao/", views.pedido_decidir_alteracao_arte, name="pedido_decidir_alteracao_arte"),
    path("<int:pk>/arquivos-oficiais/<uuid:arquivo_id>/verificar/", views.pedido_verificar_arquivo_oficial, name="pedido_verificar_arquivo_oficial"),
    path("<int:pk>/arquivos-oficiais/<uuid:arquivo_id>/vincular-restaurado/", views.pedido_vincular_arquivo_restaurado, name="pedido_vincular_arquivo_restaurado"),
    path("<int:pk>/arquivos-oficiais/<uuid:arquivo_id>/reconhecer-alerta/", views.pedido_reconhecer_alerta_arquivo, name="pedido_reconhecer_alerta_arquivo"),
    path("<int:pk>/arquivos-oficiais/<uuid:arquivo_id>/encerrar/", views.pedido_encerrar_arquivo_oficial, name="pedido_encerrar_arquivo_oficial"),
    path("<int:pk>/anexos/adicionar/", views.pedido_adicionar_anexos, name="pedido_adicionar_anexos"),
    path("<int:pk>/anexos/<uuid:anexo_id>/desvincular/", views.pedido_desvincular_anexo, name="pedido_desvincular_anexo"),
    path("<int:pk>/anexos/<uuid:anexo_id>/baixar/", views.pedido_baixar_anexo, name="pedido_baixar_anexo"),
    path("<int:pk>/status/", views.pedido_update_status, name="pedido_update_status"),
    path("<int:pk>/rejeitar-producao/", views.pedido_rejeitar_producao, name="pedido_rejeitar_producao"),
]
