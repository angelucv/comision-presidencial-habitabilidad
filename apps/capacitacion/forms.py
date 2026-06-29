from django import forms
from django.core.exceptions import ValidationError

from apps.participantes.models import Participante
from apps.participantes.venezuela import (
    CODIGOS_MOVIL_VE,
    TIPO_CEDULA_CHOICES,
    formato_cedula_numero_input,
    formato_telefono_linea_input,
    separar_cedula,
    separar_telefono,
    validar_cedula_partes,
    validar_telefono_partes,
)

from .models import Sede, Sesion


class ElegirSedeSesionForm(forms.Form):
    sede = forms.ModelChoiceField(
        queryset=Sede.objects.filter(activa=True).order_by("nombre"),
        label="Lugar de inducción",
        empty_label="— Seleccione una sede —",
    )
    sesion = forms.ModelChoiceField(
        queryset=Sesion.objects.none(),
        label="Fecha y hora",
        empty_label="— Primero elija una sede —",
    )

    def __init__(self, *args, sede_slug=None, **kwargs):
        super().__init__(*args, **kwargs)
        sede_qs = Sede.objects.filter(activa=True).order_by("nombre")
        if sede_slug:
            sede_qs = sede_qs.filter(slug=sede_slug)
            if sede_qs.exists():
                self.fields["sede"].initial = sede_qs.first()
                self.fields["sede"].widget = forms.HiddenInput()
        self.fields["sede"].queryset = sede_qs

        sede_id = None
        if self.data.get("sede"):
            sede_id = self.data.get("sede")
        elif sede_slug and sede_qs.exists():
            sede_id = sede_qs.first().pk
        elif self.initial.get("sede"):
            sede_id = self.initial["sede"]

        if sede_id:
            self.fields["sesion"].queryset = (
                Sesion.objects.filter(sede_id=sede_id, estado=Sesion.Estado.PROGRAMADA)
                .select_related("sede")
                .order_by("fecha", "hora")
            )

    def clean(self):
        cleaned = super().clean()
        sesion = cleaned.get("sesion")
        if sesion and not sesion.esta_abierta_inscripcion():
            raise ValidationError("La sesión seleccionada no tiene cupo o ya no admite inscripciones.")
        return cleaned


class DatosParticipanteForm(forms.ModelForm):
    cedula_tipo = forms.ChoiceField(
        label="Tipo",
        choices=TIPO_CEDULA_CHOICES,
        widget=forms.Select(attrs={"class": "form-select", "id": "id_cedula_tipo"}),
    )
    cedula_numero = forms.CharField(
        label="Número de cédula",
        max_length=12,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "id": "id_cedula_numero",
                "placeholder": "12.345.678",
                "inputmode": "numeric",
                "autocomplete": "off",
            }
        ),
        help_text="Solo dígitos (6 a 9). Se formatea automáticamente.",
    )
    telefono_operadora = forms.ChoiceField(
        label="Operadora",
        choices=CODIGOS_MOVIL_VE,
        widget=forms.Select(attrs={"class": "form-select", "id": "id_telefono_operadora"}),
    )
    telefono_linea = forms.CharField(
        label="Número",
        max_length=8,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "id": "id_telefono_linea",
                "placeholder": "123-4567",
                "inputmode": "numeric",
                "autocomplete": "tel-national",
            }
        ),
        help_text="7 dígitos después del código 04XX.",
    )

    class Meta:
        model = Participante
        fields = [
            "apellidos",
            "nombres",
            "correo",
            "profesion",
            "profesion_otro",
            "procedencia",
        ]
        widgets = {
            "apellidos": forms.TextInput(attrs={"class": "form-control", "autocomplete": "family-name"}),
            "nombres": forms.TextInput(attrs={"class": "form-control", "autocomplete": "given-name"}),
            "correo": forms.EmailInput(attrs={"class": "form-control", "placeholder": "correo@ejemplo.com"}),
            "profesion": forms.Select(attrs={"class": "form-select"}),
            "profesion_otro": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Solo si eligió «Otro»"}
            ),
            "procedencia": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Universidad, institución o empresa"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            tipo, num = separar_cedula(self.instance.cedula)
            self.fields["cedula_tipo"].initial = tipo
            self.fields["cedula_numero"].initial = formato_cedula_numero_input(num)
            op, linea = separar_telefono(self.instance.telefono)
            self.fields["telefono_operadora"].initial = op
            self.fields["telefono_linea"].initial = formato_telefono_linea_input(linea)

    def clean(self):
        cleaned = super().clean()
        try:
            cleaned["cedula"] = validar_cedula_partes(
                cleaned.get("cedula_tipo", ""),
                cleaned.get("cedula_numero", ""),
            )
        except ValidationError as exc:
            self.add_error("cedula_numero", exc)

        try:
            cleaned["telefono"] = validar_telefono_partes(
                cleaned.get("telefono_operadora", ""),
                cleaned.get("telefono_linea", ""),
            )
        except ValidationError as exc:
            self.add_error("telefono_linea", exc)

        if cleaned.get("profesion") == Participante.Profesion.OTRO and not cleaned.get("profesion_otro", "").strip():
            self.add_error("profesion_otro", "Indique la profesión cuando selecciona «Otro».")
        return cleaned
