from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path
from apps.catalogo import views as catalogo_views
from config.views import home


urlpatterns = [
    path("", home, name="home"),
    path("login/", catalogo_views.login_operador, name="login"),
    path("sair/", catalogo_views.logout_operador, name="logout"),
    path("primeiro-admin/", catalogo_views.primeiro_admin, name="primeiro_admin"),
    path("", include("apps.financeiro.urls")),
    path("pedidos/", include("apps.pedidos.urls")),
    path("produtos/", catalogo_views.produtos, name="produtos"),
    path("produtos/<int:pk>/editar/", catalogo_views.produto_editar, name="produto_editar"),
    path("produtos/<int:pk>/excluir/", catalogo_views.produto_excluir, name="produto_excluir"),
    path("categorias/<int:pk>/excluir/", catalogo_views.categoria_excluir, name="categoria_excluir"),
    path("assistencia-envio/", catalogo_views.assistencia_envio, name="assistencia_envio"),
    path("assistencia-envio/<int:pk>/enviado/", catalogo_views.assistencia_marcar_enviado, name="assistencia_marcar_enviado"),
    path("configuracoes/", catalogo_views.configuracoes, name="configuracoes"),
    path("producao/login/", catalogo_views.login_producao, name="producao_login"),
    path("producao/", catalogo_views.producao_home, name="producao_home"),
    path("producao/configuracoes/", catalogo_views.producao_configuracoes, name="producao_configuracoes"),
    path("api/widgets/prazos/", catalogo_views.api_widget_prazos, name="api_widget_prazos"),
    path("api/notificacoes/assistencia/", catalogo_views.api_notificacao_assistencia, name="api_notificacao_assistencia"),
    path("api/preferencias/", catalogo_views.api_preferencias, name="api_preferencias"),
    path("api/launcher/login/", catalogo_views.api_launcher_login, name="api_launcher_login"),
    path("api/launcher/trocar-senha/", catalogo_views.api_launcher_trocar_senha, name="api_launcher_trocar_senha"),
    path("api/launcher/recuperar-senha/", catalogo_views.api_launcher_recuperar_senha, name="api_launcher_recuperar_senha"),
    path("admin/", admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()
