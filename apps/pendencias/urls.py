from django.urls import path

from .views import lista_pendencias

urlpatterns = [path("", lista_pendencias, name="pendencias_lista")]
