from django import forms

from apps.inspecciones.models import Edificacion
from apps.inspecciones.venezuela_geo import ESTADOS_VE


class EdificacionForm(forms.ModelForm):
    class Meta:
        model = Edificacion
        fields = [
            "nombre",
            "direccion",
            "municipio",
            "estado",
            "latitud",
            "longitud",
            "notas",
        ]
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
            "direccion": forms.TextInput(attrs={"class": "form-control"}),
            "municipio": forms.TextInput(attrs={"class": "form-control"}),
            "estado": forms.Select(attrs={"class": "form-select"}, choices=ESTADOS_VE),
            "latitud": forms.NumberInput(attrs={"class": "form-control", "step": "any"}),
            "longitud": forms.NumberInput(attrs={"class": "form-control", "step": "any"}),
            "notas": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
        }
