from django.urls import path

from .views import estacoes, identidade_atual, incorporar, painel


urlpatterns = [
    path("", painel, name="sincronizacao_painel"),
    path("incorporar/", incorporar, name="sincronizacao_incorporar"),
    path("estacoes/", estacoes, name="sincronizacao_estacoes"),
    path("identidade-atual/", identidade_atual, name="sincronizacao_identidade_atual"),
]
