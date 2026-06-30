from django.shortcuts import render

from apps.capacitacion.decorators import coordinador_required
from apps.inspecciones.models import Edificacion
from apps.inspecciones.venezuela_geo import MAPA_CENTRO_LAT, MAPA_CENTRO_LON, MAPA_ZOOM_INICIAL


@coordinador_required
def mapa_edificios(request):
    edificaciones = Edificacion.objects.exclude(latitud__isnull=True).exclude(longitud__isnull=True)
    puntos = []
    for ed in edificaciones:
        puntos.append(
            {
                "codigo": ed.codigo,
                "nombre": ed.nombre,
                "direccion": ed.direccion,
                "municipio": ed.municipio,
                "estado": ed.estado,
                "lat": float(ed.latitud),
                "lon": float(ed.longitud),
                "semaforo": ed.semaforo or "pendiente",
                "estado_inspeccion": ed.estado_inspeccion,
                "url": f"/inspecciones/edificios/{ed.pk}/",
            }
        )
    stats = {
        "total": Edificacion.objects.count(),
        "pendientes": Edificacion.objects.filter(estado_inspeccion=Edificacion.Estado.PENDIENTE).count(),
        "inspeccionados": Edificacion.objects.filter(estado_inspeccion=Edificacion.Estado.INSPECCIONADO).count(),
        "rojos": Edificacion.objects.filter(semaforo=Edificacion.Semaforo.ROJO).count(),
        "amarillos": Edificacion.objects.filter(semaforo=Edificacion.Semaforo.AMARILLO).count(),
        "verdes": Edificacion.objects.filter(semaforo=Edificacion.Semaforo.VERDE).count(),
    }
    return render(
        request,
        "reportes/mapa_edificios.html",
        {
            "puntos": puntos,
            "centro_lat": MAPA_CENTRO_LAT,
            "centro_lon": MAPA_CENTRO_LON,
            "zoom": MAPA_ZOOM_INICIAL,
            "stats": stats,
        },
    )
