from django.contrib import admin
from django.utils.html import format_html

from .models import Campana, Inscripcion, Sede, Sesion


class SesionInline(admin.TabularInline):
    model = Sesion
    extra = 0
    fields = ("fecha", "hora", "cupo", "estado", "responsable_nombre")


@admin.register(Campana)
class CampanaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "activa", "fecha_inicio", "fecha_fin", "responsable_nombre")
    list_filter = ("activa",)


@admin.register(Sede)
class SedeAdmin(admin.ModelAdmin):
    list_display = ("nombre", "slug", "campana", "municipio", "estado", "activa", "qr_link")
    list_filter = ("activa", "campana", "estado")
    search_fields = ("nombre", "slug", "direccion")
    prepopulated_fields = {"slug": ("nombre",)}
    inlines = [SesionInline]

    @admin.display(description="QR / enlace")
    def qr_link(self, obj):
        return format_html(
            '<a href="/inscripcion/sede/{}/" target="_blank">/inscripcion/sede/{}/</a>',
            obj.slug,
            obj.slug,
        )


class InscripcionInline(admin.TabularInline):
    model = Inscripcion
    extra = 0
    readonly_fields = ("codigo", "participante", "creado_en")
    can_delete = False


@admin.register(Sesion)
class SesionAdmin(admin.ModelAdmin):
    list_display = (
        "sede",
        "fecha",
        "hora",
        "cupo",
        "inscritos_display",
        "estado",
        "responsable_nombre",
    )
    list_filter = ("estado", "fecha", "sede")
    search_fields = ("sede__nombre",)
    date_hierarchy = "fecha"
    inlines = [InscripcionInline]

    @admin.display(description="Inscritos")
    def inscritos_display(self, obj):
        return f"{obj.inscritos_count} / {obj.cupo}"


@admin.register(Inscripcion)
class InscripcionAdmin(admin.ModelAdmin):
    list_display = (
        "codigo",
        "participante",
        "sesion",
        "asistio",
        "certificado_emitido",
        "creado_en",
    )
    list_filter = ("asistio", "certificado_emitido", "sesion__sede", "sesion__fecha")
    search_fields = ("codigo", "participante__cedula", "participante__apellidos", "participante__nombres")
    readonly_fields = ("codigo", "creado_en")
    autocomplete_fields = ("participante", "sesion")
