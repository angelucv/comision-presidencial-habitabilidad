from django import forms

from .models import Campana


class ImportarExcelForm(forms.Form):
    archivo = forms.FileField(
        label="Archivo Excel (.xlsx)",
        help_text='Hojas "sedes" y/o "sesiones". Descargue la plantilla antes de cargar.',
    )
    campana = forms.ModelChoiceField(
        queryset=Campana.objects.filter(activa=True),
        required=False,
        label="Campaña (solo para hoja sedes)",
        empty_label="— Sin campaña —",
    )

    def clean_archivo(self):
        f = self.cleaned_data["archivo"]
        if not f.name.lower().endswith(".xlsx"):
            raise forms.ValidationError("Solo se aceptan archivos .xlsx")
        if f.size > 5 * 1024 * 1024:
            raise forms.ValidationError("El archivo no puede superar 5 MB.")
        return f
