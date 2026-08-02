from django.urls import path
from . import views

urlpatterns = [path("", views.lista_missoes, name="missoes_lista"), path("nova/", views.criar_missao, name="missao_criar"), path("<uuid:missao_id>/", views.detalhe_missao, name="missao_detalhe")]
