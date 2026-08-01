from django.urls import path

from apps.auditoria import views


urlpatterns = [path("", views.auditoria_lista, name="auditoria_lista")]
