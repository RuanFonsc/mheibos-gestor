from django.urls import path

from apps.aprendizado import views
from apps.aprendizado import knowledge_views


urlpatterns = [
    path("", views.aprendizado_home, name="aprendizado_home"),
    path("exportar-json/", views.aprendizado_exportar_json, name="aprendizado_exportar_json"),
    path("webhook/evolution/", views.evolution_webhook, name="evolution_webhook"),
    path("conhecimento/", knowledge_views.conhecimento_lista, name="conhecimento_lista"),
    path("conhecimento/registrar/", knowledge_views.conhecimento_registrar, name="conhecimento_registrar"),
    path("conhecimento/<int:conhecimento_id>/aprovar/", knowledge_views.conhecimento_aprovar, name="conhecimento_aprovar"),
]
