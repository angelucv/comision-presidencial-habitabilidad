from django.urls import path

from . import views

app_name = "inspecciones"

urlpatterns = [
    path("", views.inicio, name="inicio"),
    path("edificios/", views.lista_edificios, name="lista_edificios"),
    path("edificios/<int:edificacion_id>/", views.detalle_edificio, name="detalle_edificio"),
    path(
        "edificios/<int:edificacion_id>/nueva/",
        views.nueva_inspeccion,
        name="nueva_inspeccion",
    ),
    path("wizard/<int:inspeccion_id>/", views.wizard_inspeccion, name="wizard"),
]
