from django.urls import path
from . import views

urlpatterns = [
    path("", views.lista_missoes, name="missoes_lista"),
    path("nova/", views.criar_missao, name="missao_criar"),
    path("<uuid:missao_id>/", views.detalhe_missao, name="missao_detalhe"),
    path("<uuid:missao_id>/<str:acao>/", views.alterar_estado_missao, name="missao_alterar_estado"),
]
