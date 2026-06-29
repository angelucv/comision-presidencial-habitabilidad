from django.urls import path

from . import views

app_name = "reportes"

urlpatterns = [
    path("mapa/", views.mapa_edificios, name="mapa_edificios"),
]
