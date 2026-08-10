from django.urls import path
from . import views

urlpatterns = [
    path("", views.lista_missoes, name="missoes_lista"),
    path("nova/", views.criar_missao, name="missao_criar"),
    path("nova-coletiva/", views.criar_missao_coletiva, name="missao_criar_coletiva"),
    path("<uuid:missao_id>/", views.detalhe_missao, name="missao_detalhe"),
    path("workspace/<uuid:missao_id>/", views.detalhe_missao, name="missao_workspace"),
    path("<uuid:missao_id>/convidar/", views.convidar_na_missao, name="missao_convidar"),
    path("<uuid:missao_id>/tarefas/adicionar/", views.adicionar_tarefa_view, name="missao_tarefa_adicionar"),
    path("tarefas/<uuid:tarefa_id>/concluir/", views.concluir_tarefa_view, name="missao_tarefa_concluir"),
    path("<uuid:missao_id>/notas/adicionar/", views.adicionar_nota_view, name="missao_nota_adicionar"),
    path("<uuid:missao_id>/chat/enviar/", views.enviar_chat_view, name="missao_chat_enviar"),
    path("participacoes/<uuid:participacao_id>/<str:resposta>/", views.responder_convite_view, name="missao_responder_convite"),
    path("participacoes/<uuid:participacao_id>/manifestar/", views.manifestar_convite_view, name="missao_manifestar_convite"),
    path("participacoes/<uuid:participacao_id>/sair/", views.sair_missao_view, name="missao_sair"),
    path("<uuid:missao_id>/<str:acao>/", views.alterar_estado_missao, name="missao_alterar_estado"),
]
