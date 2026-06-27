from django.urls import path

from apps.pedidos import views


urlpatterns = [
    path("", views.pedido_list, name="pedido_list"),
    path("novo/", views.pedido_create, name="pedido_create"),
    path("<int:pk>/", views.pedido_detail, name="pedido_detail"),
    path("<int:pk>/editar/", views.pedido_edit, name="pedido_edit"),
    path("<int:pk>/status/", views.pedido_update_status, name="pedido_update_status"),
]
