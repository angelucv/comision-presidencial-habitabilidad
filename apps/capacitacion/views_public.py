from django.contrib import messages
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from apps.participantes.models import Participante

from .forms import DatosParticipanteForm, ElegirSedeSesionForm
from .models import Inscripcion, Sede, Sesion
from .services import enviar_correo_confirmacion


@require_http_methods(["GET", "POST"])
def inscripcion_paso1(request):
    form = ElegirSedeSesionForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        return redirect("capacitacion_public:paso2", sesion_id=form.cleaned_data["sesion"].pk)
    return render(
        request,
        "capacitacion/inscripcion_paso1.html",
        {"form": form, "titulo": "Inscripción — elegir sede y sesión"},
    )


@require_http_methods(["GET", "POST"])
def inscripcion_por_sede(request, slug):
    sede = get_object_or_404(Sede, slug=slug, activa=True)
    form = ElegirSedeSesionForm(request.POST or None, sede_slug=slug)
    if request.method == "POST" and form.is_valid():
        return redirect("capacitacion_public:paso2", sesion_id=form.cleaned_data["sesion"].pk)
    return render(
        request,
        "capacitacion/inscripcion_paso1.html",
        {
            "form": form,
            "sede": sede,
            "titulo": f"Inscripción — {sede.nombre}",
            "qr_mode": True,
        },
    )


@require_http_methods(["GET", "POST"])
def inscripcion_paso2(request, sesion_id):
    sesion = get_object_or_404(
        Sesion.objects.select_related("sede"),
        pk=sesion_id,
        estado=Sesion.Estado.PROGRAMADA,
    )
    if not sesion.esta_abierta_inscripcion():
        messages.error(request, "Esta sesión ya no admite inscripciones.")
        return redirect("capacitacion_public:paso1")

    form = DatosParticipanteForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        with transaction.atomic():
            cedula = form.cleaned_data["cedula"]
            participante, _ = Participante.objects.update_or_create(
                cedula=cedula,
                defaults={
                    "apellidos": form.cleaned_data["apellidos"],
                    "nombres": form.cleaned_data["nombres"],
                    "telefono": form.cleaned_data["telefono"],
                    "correo": form.cleaned_data.get("correo", ""),
                    "profesion": form.cleaned_data["profesion"],
                    "profesion_otro": form.cleaned_data.get("profesion_otro", ""),
                    "procedencia": form.cleaned_data["procedencia"],
                },
            )
            if Inscripcion.objects.filter(sesion=sesion, participante=participante).exists():
                messages.warning(request, "Ya estaba inscrito en esta sesión.")
                inscripcion = Inscripcion.objects.get(sesion=sesion, participante=participante)
            else:
                inscripcion = Inscripcion.objects.create(sesion=sesion, participante=participante)
        try:
            if enviar_correo_confirmacion(inscripcion, request):
                messages.info(request, "Se envió un correo de confirmación.")
        except Exception:
            messages.warning(
                request,
                "Inscripción guardada, pero no se pudo enviar el correo. Verifique la configuración SMTP.",
            )
        return redirect("capacitacion_public:confirmacion", codigo=inscripcion.codigo)

    return render(
        request,
        "capacitacion/inscripcion_paso2.html",
        {"form": form, "sesion": sesion},
    )


def inscripcion_confirmacion(request, codigo):
    inscripcion = get_object_or_404(
        Inscripcion.objects.select_related("sesion__sede", "participante"),
        codigo=codigo,
    )
    return render(request, "capacitacion/inscripcion_confirmacion.html", {"inscripcion": inscripcion})
