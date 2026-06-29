from django.contrib import messages
from django.db.models import Count
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_http_methods

from apps.inspecciones.forms import EdificacionForm
from apps.inspecciones.models import Edificacion

from .certificacion import certificar_inscripcion
from .decorators import coordinador_required
from .forms_panel import ImportarExcelForm
from .models import Campana, Inscripcion, Sede, Sesion
from .services import (
    exportar_inscritos_sesion,
    generar_plantilla_excel,
    generar_qr_png,
    importar_excel_completo,
    inscripcion_url_por_sede,
)


@coordinador_required
def panel_inicio(request):
    hoy = timezone.localdate()
    campana_activa = Campana.objects.filter(activa=True).first()
    stats = {
        "sedes": Sede.objects.filter(activa=True).count(),
        "sesiones": Sesion.objects.filter(estado=Sesion.Estado.PROGRAMADA).count(),
        "inscripciones": Inscripcion.objects.count(),
        "sesiones_hoy": Sesion.objects.filter(fecha=hoy, estado=Sesion.Estado.PROGRAMADA).count(),
    }
    sesiones_proximas = (
        Sesion.objects.filter(fecha__gte=hoy, estado=Sesion.Estado.PROGRAMADA)
        .select_related("sede")
        .annotate(num_inscritos=Count("inscripciones"))
        .order_by("fecha", "hora")[:10]
    )
    return render(
        request,
        "capacitacion/panel/inicio.html",
        {
            "stats": stats,
            "campana_activa": campana_activa,
            "sesiones_proximas": sesiones_proximas,
        },
    )


@coordinador_required
def panel_sedes(request):
    sedes = Sede.objects.filter(activa=True).select_related("campana").order_by("nombre")
    return render(request, "capacitacion/panel/sedes.html", {"sedes": sedes})


@coordinador_required
def panel_sede_qr(request, sede_id):
    sede = get_object_or_404(Sede, pk=sede_id, activa=True)
    url = inscripcion_url_por_sede(sede, request)
    png = generar_qr_png(url)
    response = HttpResponse(png, content_type="image/png")
    response["Content-Disposition"] = f'attachment; filename="qr-inscripcion-{sede.slug}.png"'
    return response


@coordinador_required
def panel_sesiones(request):
    sesiones = (
        Sesion.objects.select_related("sede")
        .annotate(num_inscritos=Count("inscripciones"))
        .order_by("-fecha", "hora")[:50]
    )
    return render(request, "capacitacion/panel/sesiones.html", {"sesiones": sesiones})


@coordinador_required
def panel_sesion_asistencia(request, sesion_id):
    sesion = get_object_or_404(Sesion.objects.select_related("sede"), pk=sesion_id)
    inscripciones = (
        Inscripcion.objects.filter(sesion=sesion)
        .select_related("participante")
        .order_by("participante__apellidos", "participante__nombres")
    )
    return render(
        request,
        "capacitacion/panel/sesion_asistencia.html",
        {"sesion": sesion, "inscripciones": inscripciones},
    )


@coordinador_required
@require_http_methods(["POST"])
def panel_marcar_asistencia(request, inscripcion_id):
    inscripcion = get_object_or_404(Inscripcion, pk=inscripcion_id)
    inscripcion.asistio = request.POST.get("asistio") == "1"
    inscripcion.save(update_fields=["asistio"])
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return JsonResponse({"ok": True, "asistio": inscripcion.asistio})
    messages.success(request, f"Asistencia actualizada — {inscripcion.participante.nombre_completo}")
    return redirect("capacitacion:panel_sesion_asistencia", sesion_id=inscripcion.sesion_id)


@coordinador_required
@require_http_methods(["POST"])
def panel_certificar_inscripcion(request, inscripcion_id):
    inscripcion = get_object_or_404(
        Inscripcion.objects.select_related("participante", "sesion__sede"),
        pk=inscripcion_id,
    )
    if inscripcion.certificado_emitido:
        messages.info(request, "Esta inscripción ya estaba certificada.")
        return redirect("capacitacion:panel_sesion_asistencia", sesion_id=inscripcion.sesion_id)

    encargado = request.POST.get("encargado_charla", "").strip()
    user, clave, correo_ok = certificar_inscripcion(
        inscripcion,
        request.user,
        encargado_charla=encargado,
        request=request,
    )
    if correo_ok:
        messages.success(
            request,
            f"Certificado emitido para {inscripcion.participante.nombre_completo}. "
            f"Usuario «{user.username}» enviado por correo.",
        )
    elif inscripcion.participante.correo:
        messages.warning(
            request,
            f"Certificado registrado y usuario «{user.username}» creado, "
            f"pero no se pudo enviar el correo. Clave temporal: {clave}",
        )
    else:
        messages.warning(
            request,
            f"Certificado registrado. Usuario: {user.username} · Clave temporal: {clave} "
            f"(sin correo del participante).",
        )
    return redirect("capacitacion:panel_sesion_asistencia", sesion_id=inscripcion.sesion_id)


@coordinador_required
@require_http_methods(["GET", "POST"])
def panel_edificios(request):
    form = EdificacionForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Edificación registrada correctamente.")
        return redirect("capacitacion:panel_edificios")
    edificaciones = Edificacion.objects.order_by("-creado_en")[:50]
    return render(
        request,
        "capacitacion/panel/edificios.html",
        {"form": form, "edificaciones": edificaciones},
    )


@coordinador_required
def panel_exportar_inscritos(request, sesion_id):
    sesion = get_object_or_404(Sesion.objects.select_related("sede"), pk=sesion_id)
    data = exportar_inscritos_sesion(sesion)
    nombre = f"inscritos-{sesion.sede.slug}-{sesion.fecha}.xlsx"
    response = HttpResponse(
        data,
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    response["Content-Disposition"] = f'attachment; filename="{nombre}"'
    return response


@coordinador_required
@require_http_methods(["GET", "POST"])
def panel_importar(request):
    form = ImportarExcelForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        try:
            resultado = importar_excel_completo(
                form.cleaned_data["archivo"],
                campana=form.cleaned_data.get("campana"),
            )
            partes = []
            if resultado.get("sedes"):
                s = resultado["sedes"]
                partes.append(f"sedes: {s['creadas']} nuevas, {s['actualizadas']} actualizadas")
            if resultado.get("sesiones"):
                s = resultado["sesiones"]
                partes.append(f"sesiones: {s['creadas']} nuevas, {s['omitidas']} duplicadas")
                if s.get("errores"):
                    partes.append(f"{s['errores']} filas con error")
            messages.success(request, "Importación completada — " + "; ".join(partes))
            if resultado.get("sesiones", {}).get("detalle_errores"):
                for err in resultado["sesiones"]["detalle_errores"]:
                    messages.warning(request, err)
            return redirect("capacitacion:panel_importar")
        except ValueError as exc:
            messages.error(request, str(exc))
    return render(request, "capacitacion/panel/importar.html", {"form": form})


@coordinador_required
def panel_plantilla_excel(request):
    data = generar_plantilla_excel()
    response = HttpResponse(
        data,
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    response["Content-Disposition"] = 'attachment; filename="cpeh-plantilla-sedes-sesiones.xlsx"'
    return response
