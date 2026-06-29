from django.contrib import admin

from .models import Participante


@admin.register(Participante)
class ParticipanteAdmin(admin.ModelAdmin):
    list_display = ("cedula", "apellidos", "nombres", "profesion", "procedencia", "telefono")
    search_fields = ("cedula", "apellidos", "nombres", "correo", "procedencia")
    list_filter = ("profesion",)
