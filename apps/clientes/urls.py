from django.urls import path

from apps.clientes import views


urlpatterns = [
    path("", views.clientes, name="clientes"),
    path("<int:pk>/excluir/", views.cliente_excluir, name="cliente_excluir"),
]
