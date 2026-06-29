from django.contrib import admin

from .models import Edificacion, Inspeccion


@admin.register(Edificacion)
class EdificacionAdmin(admin.ModelAdmin):
    list_display = ("codigo", "nombre", "municipio", "estado", "estado_inspeccion", "semaforo")
    list_filter = ("estado", "estado_inspeccion", "semaforo")
    search_fields = ("codigo", "nombre", "direccion", "municipio")


@admin.register(Inspeccion)
class InspeccionAdmin(admin.ModelAdmin):
    list_display = ("pk", "edificacion", "inspector", "estado", "semaforo", "iniciada_en")
    list_filter = ("estado", "semaforo")
    raw_id_fields = ("edificacion", "inspector")
