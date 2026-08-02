from django.urls import path

from .views import incorporar, painel


urlpatterns = [
    path("", painel, name="sincronizacao_painel"),
    path("incorporar/", incorporar, name="sincronizacao_incorporar"),
]
