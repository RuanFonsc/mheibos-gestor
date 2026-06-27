from django.urls import path

from apps.financeiro import views


urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),
]
