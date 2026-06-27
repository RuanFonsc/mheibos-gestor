from django.urls import path

from apps.catalogo import views


urlpatterns = [
    path("", views.configuracoes, name="configuracoes"),
    path("produtos/", views.produtos, name="produtos"),
]
