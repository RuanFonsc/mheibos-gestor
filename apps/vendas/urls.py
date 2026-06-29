from django.urls import path

from apps.vendas import views


urlpatterns = [
    path("", views.vendas_dashboard, name="vendas_home"),
    path("dashboard/", views.vendas_dashboard, name="vendas_dashboard"),
    path("pedidos/", views.vendas_pedidos, name="vendas_pedidos"),
    path("configuracoes/", views.vendas_configuracoes, name="vendas_configuracoes"),
    path("relatorio/<str:tipo>/", views.vendas_relatorio, name="vendas_relatorio"),
    path("pedido/novo/", views.vendas_pedido_novo, name="vendas_pedido_novo"),
]
