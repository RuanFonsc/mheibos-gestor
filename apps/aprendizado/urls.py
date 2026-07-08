from django.urls import path

from apps.aprendizado import views


urlpatterns = [
    path("", views.aprendizado_home, name="aprendizado_home"),
    path("exportar-json/", views.aprendizado_exportar_json, name="aprendizado_exportar_json"),
    path("webhook/evolution/", views.evolution_webhook, name="evolution_webhook"),
]
