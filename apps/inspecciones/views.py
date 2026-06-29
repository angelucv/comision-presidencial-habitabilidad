from django.contrib import messages
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_http_methods

from apps.cuentas.inspectores import participante_certificado
from apps.inspecciones.decorators import inspector_required
from apps.inspecciones.forms import EdificacionForm
from apps.inspecciones.models import Edificacion, Inspeccion


@inspector_required
def inicio(request):
    participante = participante_certificado(request.user)
    edificaciones_pendientes = Edificacion.objects.filter(
        estado_inspeccion__in=[
            Edificacion.Estado.PENDIENTE,
            Edificacion.Estado.ASIGNADO,
        ]
    ).count()
    mis_inspecciones = Inspeccion.objects.filter(inspector=request.user).count()
    inspecciones_activas = Inspeccion.objects.filter(
        inspector=request.user,
        estado=Inspeccion.Estado.BORRADOR,
    ).select_related("edificacion")[:5]
    return render(
        request,
        "inspecciones/inicio.html",
        {
            "participante": participante,
            "edificaciones_pendientes": edificaciones_pendientes,
            "mis_inspecciones": mis_inspecciones,
            "inspecciones_activas": inspecciones_activas,
        },
    )


@inspector_required
def lista_edificios(request):
    q = request.GET.get("q", "").strip()
    estado_filtro = request.GET.get("estado", "")
    edificaciones = Edificacion.objects.all()
    if q:
        edificaciones = edificaciones.filter(
            Q(nombre__icontains=q)
            | Q(direccion__icontains=q)
            | Q(municipio__icontains=q)
            | Q(codigo__icontains=q)
        )
    if estado_filtro:
        edificaciones = edificaciones.filter(estado_inspeccion=estado_filtro)
    return render(
        request,
        "inspecciones/lista_edificios.html",
        {
            "edificaciones": edificaciones.order_by("estado", "nombre")[:100],
            "q": q,
            "estado_filtro": estado_filtro,
            "estados": Edificacion.Estado.choices,
        },
    )


@inspector_required
def detalle_edificio(request, edificacion_id):
    edificacion = get_object_or_404(Edificacion, pk=edificacion_id)
    inspecciones = edificacion.inspecciones.select_related("inspector").order_by("-iniciada_en")[:10]
    inspeccion_activa = Inspeccion.objects.filter(
        edificacion=edificacion,
        inspector=request.user,
        estado=Inspeccion.Estado.BORRADOR,
    ).first()
    return render(
        request,
        "inspecciones/detalle_edificio.html",
        {
            "edificacion": edificacion,
            "inspecciones": inspecciones,
            "inspeccion_activa": inspeccion_activa,
        },
    )


@inspector_required
@require_http_methods(["GET", "POST"])
def nueva_inspeccion(request, edificacion_id):
    edificacion = get_object_or_404(Edificacion, pk=edificacion_id)
    existente = Inspeccion.objects.filter(
        edificacion=edificacion,
        inspector=request.user,
        estado=Inspeccion.Estado.BORRADOR,
    ).first()
    if existente:
        return redirect("inspecciones:wizard", inspeccion_id=existente.pk)

    if request.method == "POST":
        inspeccion = Inspeccion.objects.create(
            edificacion=edificacion,
            inspector=request.user,
            paso_actual=0,
            datos={
                "paso_0": {
                    "inspector_nombre": request.user.get_full_name() or request.user.username,
                    "fecha": timezone.localdate().isoformat(),
                }
            },
        )
        if edificacion.estado_inspeccion == Edificacion.Estado.PENDIENTE:
            edificacion.estado_inspeccion = Edificacion.Estado.ASIGNADO
            edificacion.inspector_asignado = request.user
            edificacion.save(update_fields=["estado_inspeccion", "inspector_asignado", "actualizado_en"])
        return redirect("inspecciones:wizard", inspeccion_id=inspeccion.pk)

    participante = participante_certificado(request.user)
    return render(
        request,
        "inspecciones/nueva_inspeccion.html",
        {"edificacion": edificacion, "participante": participante},
    )


@inspector_required
@require_http_methods(["GET", "POST"])
def wizard_inspeccion(request, inspeccion_id):
    inspeccion = get_object_or_404(
        Inspeccion.objects.select_related("edificacion"),
        pk=inspeccion_id,
        inspector=request.user,
    )
    paso = inspeccion.paso_actual

    if request.method == "POST":
        accion = request.POST.get("accion", "siguiente")
        datos = dict(inspeccion.datos)
        paso_key = f"paso_{paso}"
        datos[paso_key] = {
            "notas": request.POST.get("notas", "").strip(),
            "riesgo_externo": request.POST.get("riesgo_externo", ""),
        }
        inspeccion.datos = datos

        if accion == "anterior" and paso > 0:
            inspeccion.paso_actual = paso - 1
        elif accion == "siguiente" and paso < 8:
            inspeccion.paso_actual = paso + 1
        elif accion == "cerrar":
            semaforo = request.POST.get("semaforo", "")
            if semaforo in Edificacion.Semaforo.values:
                inspeccion.semaforo = semaforo
                inspeccion.estado = Inspeccion.Estado.COMPLETADA
                inspeccion.completada_en = timezone.now()
                inspeccion.observaciones_cierre = request.POST.get("observaciones_cierre", "")
                ed = inspeccion.edificacion
                ed.semaforo = semaforo
                ed.estado_inspeccion = Edificacion.Estado.INSPECCIONADO
                ed.save(update_fields=["semaforo", "estado_inspeccion", "actualizado_en"])
                messages.success(request, "Inspección completada y registrada en el mapa.")
                return redirect("inspecciones:detalle_edificio", edificacion_id=ed.pk)
        inspeccion.save()
        return redirect("inspecciones:wizard", inspeccion_id=inspeccion.pk)

    titulos_pasos = [
        "0 — Información general",
        "1 — Inspección externa",
        "2 — Piso crítico y elementos estructurales",
        "3 — Inspección interna",
        "4 — Daños no estructurales",
        "5 — Evaluación de riesgo",
        "6 — Etiqueta y acceso",
        "7 — Recomendaciones",
        "8 — Cierre y firma",
    ]
    return render(
        request,
        "inspecciones/wizard.html",
        {
            "inspeccion": inspeccion,
            "edificacion": inspeccion.edificacion,
            "paso": paso,
            "titulo_paso": titulos_pasos[paso] if paso < len(titulos_pasos) else f"Paso {paso}",
            "total_pasos": 8,
            "semaforos": Edificacion.Semaforo.choices,
            "datos_paso": inspeccion.datos.get(f"paso_{paso}", {}),
        },
    )
