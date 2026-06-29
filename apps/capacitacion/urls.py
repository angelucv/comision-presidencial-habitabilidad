from django.urls import path

from . import views_panel

app_name = "capacitacion"

urlpatterns = [
    path("", views_panel.panel_inicio, name="panel_inicio"),
    path("sedes/", views_panel.panel_sedes, name="panel_sedes"),
    path("sedes/<int:sede_id>/qr.png", views_panel.panel_sede_qr, name="panel_sede_qr"),
    path("sesiones/", views_panel.panel_sesiones, name="panel_sesiones"),
    path(
        "sesiones/<int:sesion_id>/asistencia/",
        views_panel.panel_sesion_asistencia,
        name="panel_sesion_asistencia",
    ),
    path(
        "inscripciones/<int:inscripcion_id>/asistencia/",
        views_panel.panel_marcar_asistencia,
        name="panel_marcar_asistencia",
    ),
    path(
        "inscripciones/<int:inscripcion_id>/certificar/",
        views_panel.panel_certificar_inscripcion,
        name="panel_certificar_inscripcion",
    ),
    path("edificios/", views_panel.panel_edificios, name="panel_edificios"),
    path(
        "sesiones/<int:sesion_id>/exportar/",
        views_panel.panel_exportar_inscritos,
        name="panel_exportar_inscritos",
    ),
    path("importar/", views_panel.panel_importar, name="panel_importar"),
    path("plantilla-excel/", views_panel.panel_plantilla_excel, name="panel_plantilla_excel"),
]
