from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from apps.catalogo import views as catalogo_views
from config.views import home


urlpatterns = [
    path("", home, name="home"),
    path("", include("apps.financeiro.urls")),
    path("pedidos/", include("apps.pedidos.urls")),
    path("produtos/", catalogo_views.produtos, name="produtos"),
    path("produtos/<int:pk>/editar/", catalogo_views.produto_editar, name="produto_editar"),
    path("assistencia-envio/", catalogo_views.assistencia_envio, name="assistencia_envio"),
    path("assistencia-envio/<int:pk>/enviado/", catalogo_views.assistencia_marcar_enviado, name="assistencia_marcar_enviado"),
    path("configuracoes/", catalogo_views.configuracoes, name="configuracoes"),
    path("api/widgets/prazos/", catalogo_views.api_widget_prazos, name="api_widget_prazos"),
    path("api/notificacoes/assistencia/", catalogo_views.api_notificacao_assistencia, name="api_notificacao_assistencia"),
    path("api/preferencias/", catalogo_views.api_preferencias, name="api_preferencias"),
    path("admin/", admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
