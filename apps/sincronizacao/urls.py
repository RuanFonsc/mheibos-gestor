from django.urls import path

from .views import estacoes, incorporar, painel


urlpatterns = [
    path("", painel, name="sincronizacao_painel"),
    path("incorporar/", incorporar, name="sincronizacao_incorporar"),
    path("estacoes/", estacoes, name="sincronizacao_estacoes"),
]
