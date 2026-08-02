from django.urls import path

from .views import resumo_pedido


urlpatterns = [
    path("pedidos/<int:pk>/resumo/", resumo_pedido, name="cognicao_resumo_pedido")
]
