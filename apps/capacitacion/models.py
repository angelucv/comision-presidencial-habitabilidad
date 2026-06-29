from django.db import models
from django.utils import timezone
from django.utils.text import slugify


class Campana(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    activa = models.BooleanField(default=True)
    fecha_inicio = models.DateField(null=True, blank=True)
    fecha_fin = models.DateField(null=True, blank=True)
    responsable_nombre = models.CharField("Responsable por defecto", max_length=200, blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-activa", "-fecha_inicio", "nombre"]
        verbose_name = "campaña"
        verbose_name_plural = "campañas"

    def __str__(self) -> str:
        return self.nombre


class Sede(models.Model):
    campana = models.ForeignKey(
        Campana,
        on_delete=models.CASCADE,
        related_name="sedes",
        null=True,
        blank=True,
    )
    nombre = models.CharField("Lugar de inducción", max_length=200)
    slug = models.SlugField(max_length=80, unique=True)
    direccion = models.CharField(max_length=300, blank=True)
    municipio = models.CharField(max_length=100, blank=True)
    estado = models.CharField(max_length=100, blank=True)
    responsable_nombre = models.CharField(max_length=200, blank=True)
    activa = models.BooleanField(default=True)
    notas = models.TextField(blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["nombre"]
        verbose_name = "sede"
        verbose_name_plural = "sedes"

    def __str__(self) -> str:
        return self.nombre

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.nombre)[:70] or "sede"
            slug = base
            n = 1
            while Sede.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base}-{n}"
                n += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def responsable_efectivo(self) -> str:
        return self.responsable_nombre or (self.campana.responsable_nombre if self.campana else "")


class Sesion(models.Model):
    class Estado(models.TextChoices):
        PROGRAMADA = "programada", "Programada"
        CERRADA = "cerrada", "Cerrada"
        CANCELADA = "cancelada", "Cancelada"

    sede = models.ForeignKey(Sede, on_delete=models.CASCADE, related_name="sesiones")
    fecha = models.DateField("Fecha de inducción")
    hora = models.TimeField("Hora")
    cupo = models.PositiveIntegerField(default=80)
    estado = models.CharField(max_length=20, choices=Estado.choices, default=Estado.PROGRAMADA)
    responsable_nombre = models.CharField(max_length=200, blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["fecha", "hora", "sede__nombre"]
        verbose_name = "sesión"
        verbose_name_plural = "sesiones"
        constraints = [
            models.UniqueConstraint(
                fields=["sede", "fecha", "hora"],
                name="uniq_sede_fecha_hora",
            )
        ]

    def __str__(self) -> str:
        return f"{self.sede.nombre} — {self.fecha} {self.hora:%H:%M}"

    @property
    def inscritos_count(self) -> int:
        return self.inscripciones.count()

    @property
    def cupos_disponibles(self) -> int:
        return max(0, self.cupo - self.inscritos_count)

    def tiene_cupo(self) -> bool:
        return self.cupos_disponibles > 0

    def esta_abierta_inscripcion(self) -> bool:
        if self.estado != self.Estado.PROGRAMADA:
            return False
        from datetime import datetime

        inicio = timezone.make_aware(datetime.combine(self.fecha, self.hora))
        return timezone.now() < inicio and self.tiene_cupo()

    def responsable_efectivo(self) -> str:
        return self.responsable_nombre or self.sede.responsable_efectivo()


class Inscripcion(models.Model):
    codigo = models.CharField(max_length=20, unique=True, editable=False)
    sesion = models.ForeignKey(Sesion, on_delete=models.CASCADE, related_name="inscripciones")
    participante = models.ForeignKey(
        "participantes.Participante",
        on_delete=models.CASCADE,
        related_name="inscripciones",
    )
    asistio = models.BooleanField(default=False)
    certificado_emitido = models.BooleanField(default=False)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-creado_en"]
        verbose_name = "inscripción"
        verbose_name_plural = "inscripciones"
        constraints = [
            models.UniqueConstraint(
                fields=["sesion", "participante"],
                name="uniq_sesion_participante",
            )
        ]

    def __str__(self) -> str:
        return f"{self.codigo} — {self.participante}"

    def save(self, *args, **kwargs):
        if not self.codigo:
            year = timezone.now().year
            last = (
                Inscripcion.objects.filter(codigo__startswith=f"INS-{year}-")
                .order_by("-codigo")
                .values_list("codigo", flat=True)
                .first()
            )
            if last:
                try:
                    n = int(last.split("-")[-1]) + 1
                except ValueError:
                    n = 1
            else:
                n = 1
            self.codigo = f"INS-{year}-{n:04d}"
        super().save(*args, **kwargs)

    @property
    def lugar_induccion(self) -> str:
        return self.sesion.sede.nombre

    @property
    def fecha_induccion(self):
        return self.sesion.fecha

    @property
    def hora_induccion(self):
        return self.sesion.hora
