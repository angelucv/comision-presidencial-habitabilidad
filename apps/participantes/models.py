import re

from django.core.exceptions import ValidationError
from django.db import models


def validar_cedula_venezolana(valor: str) -> str:
    """Formato V/E + dígitos (ej. V12345678)."""
    valor = (valor or "").strip().upper().replace(" ", "")
    if not re.match(r"^[VE]\d{6,9}$", valor):
        raise ValidationError("Use formato V o E seguido de 6 a 9 dígitos (ej. V12345678).")
    return valor


class Participante(models.Model):
    class Profesion(models.TextChoices):
        INGENIERO_CIVIL = "ingeniero_civil", "Ingeniero civil"
        INGENIERO_ESTRUCTURAL = "ingeniero_estructural", "Ingeniero estructural"
        ARQUITECTO = "arquitecto", "Arquitecto"
        INGENIERO_INDUSTRIAL = "ingeniero_industrial", "Ingeniero industrial"
        TOPOGRAFO = "topografo", "Topógrafo"
        ESTUDIANTE = "estudiante", "Estudiante"
        OTRO = "otro", "Otro"

    cedula = models.CharField("C.I.", max_length=12, unique=True, validators=[validar_cedula_venezolana])
    apellidos = models.CharField(max_length=120)
    nombres = models.CharField(max_length=120)
    telefono = models.CharField("Teléfono celular", max_length=20)
    correo = models.EmailField(
        "Correo electrónico",
        blank=True,
        help_text="Recomendado: recibirá confirmación de inscripción.",
    )
    profesion = models.CharField(
        "Profesión / ocupación",
        max_length=40,
        choices=Profesion.choices,
        default=Profesion.INGENIERO_CIVIL,
    )
    profesion_otro = models.CharField("Profesión (otro)", max_length=120, blank=True)
    procedencia = models.CharField(
        "Procedencia",
        max_length=200,
        help_text="Universidad, institución o empresa",
    )
    usuario = models.OneToOneField(
        "auth.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="participante",
    )
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["apellidos", "nombres"]
        verbose_name = "participante"
        verbose_name_plural = "participantes"

    def __str__(self) -> str:
        return f"{self.cedula} — {self.nombre_completo}"

    @property
    def nombre_completo(self) -> str:
        return f"{self.apellidos} {self.nombres}".strip()

    def clean(self):
        super().clean()
        if self.profesion == self.Profesion.OTRO and not self.profesion_otro.strip():
            raise ValidationError({"profesion_otro": "Indique la profesión cuando selecciona «Otro»."})

    def profesion_display(self) -> str:
        if self.profesion == self.Profesion.OTRO and self.profesion_otro:
            return self.profesion_otro
        return self.get_profesion_display()
