from django.conf import settings
from django.db import models
from django.utils import timezone

from .venezuela_geo import ESTADOS_VE


class Edificacion(models.Model):
    class Estado(models.TextChoices):
        PENDIENTE = "pendiente", "Pendiente de inspección"
        ASIGNADO = "asignado", "Asignado a inspector"
        INSPECCIONADO = "inspeccionado", "Inspeccionado"

    class Semaforo(models.TextChoices):
        VERDE = "verde", "Verde — Habitable"
        AMARILLO = "amarillo", "Amarillo — Acceso restringido"
        ROJO = "rojo", "Rojo — No habitable"

    codigo = models.CharField(max_length=20, unique=True, editable=False)
    nombre = models.CharField("Nombre del edificio", max_length=200)
    direccion = models.CharField("Dirección / sector", max_length=300)
    municipio = models.CharField(max_length=100)
    estado = models.CharField("Estado", max_length=50, choices=ESTADOS_VE)
    latitud = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitud = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    estado_inspeccion = models.CharField(
        max_length=20,
        choices=Estado.choices,
        default=Estado.PENDIENTE,
    )
    semaforo = models.CharField(
        max_length=10,
        choices=Semaforo.choices,
        blank=True,
    )
    inspector_asignado = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="edificaciones_asignadas",
    )
    notas = models.TextField(blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["estado", "municipio", "nombre"]
        verbose_name = "edificación"
        verbose_name_plural = "edificaciones"

    def __str__(self) -> str:
        return f"{self.codigo} — {self.nombre}"

    def save(self, *args, **kwargs):
        if not self.codigo:
            year = timezone.now().year
            last = (
                Edificacion.objects.filter(codigo__startswith=f"ED-{year}-")
                .order_by("-codigo")
                .values_list("codigo", flat=True)
                .first()
            )
            n = int(last.split("-")[-1]) + 1 if last else 1
            self.codigo = f"ED-{year}-{n:04d}"
        super().save(*args, **kwargs)

    @property
    def tiene_coordenadas(self) -> bool:
        return self.latitud is not None and self.longitud is not None


class Inspeccion(models.Model):
    class Estado(models.TextChoices):
        BORRADOR = "borrador", "En progreso"
        COMPLETADA = "completada", "Completada"

    edificacion = models.ForeignKey(
        Edificacion,
        on_delete=models.CASCADE,
        related_name="inspecciones",
    )
    inspector = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="inspecciones_realizadas",
    )
    estado = models.CharField(max_length=20, choices=Estado.choices, default=Estado.BORRADOR)
    paso_actual = models.PositiveSmallIntegerField(default=0)
    datos = models.JSONField(default=dict, blank=True)
    semaforo = models.CharField(
        max_length=10,
        choices=Edificacion.Semaforo.choices,
        blank=True,
    )
    observaciones_cierre = models.TextField(blank=True)
    iniciada_en = models.DateTimeField(auto_now_add=True)
    completada_en = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-iniciada_en"]
        verbose_name = "inspección ERD"
        verbose_name_plural = "inspecciones ERD"

    def __str__(self) -> str:
        return f"Inspección {self.pk} — {self.edificacion.codigo}"
