from django import forms
from django.core.exceptions import ValidationError

from apps.participantes.models import Participante, validar_cedula_venezolana

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
    cedula = forms.CharField(label="C.I.", max_length=12)

    class Meta:
        model = Participante
        fields = [
            "cedula",
            "apellidos",
            "nombres",
            "telefono",
            "correo",
            "profesion",
            "profesion_otro",
            "procedencia",
        ]
        widgets = {
            "profesion_otro": forms.TextInput(attrs={"placeholder": "Solo si eligió «Otro»"}),
            "procedencia": forms.TextInput(attrs={"placeholder": "Universidad, institución o empresa"}),
        }

    def clean_cedula(self):
        return validar_cedula_venezolana(self.cleaned_data["cedula"])

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("profesion") == Participante.Profesion.OTRO and not cleaned.get("profesion_otro", "").strip():
            self.add_error("profesion_otro", "Indique la profesión cuando selecciona «Otro».")
        return cleaned
