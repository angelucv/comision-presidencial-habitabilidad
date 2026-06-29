from django.urls import path

from . import views_public

app_name = "capacitacion_public"

urlpatterns = [
    path("", views_public.inscripcion_paso1, name="paso1"),
    path("sede/<slug:slug>/", views_public.inscripcion_por_sede, name="por_sede"),
    path("sesion/<int:sesion_id>/", views_public.inscripcion_paso2, name="paso2"),
    path("confirmacion/<str:codigo>/", views_public.inscripcion_confirmacion, name="confirmacion"),
]
