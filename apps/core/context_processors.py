from django.conf import settings


def cpeh(request):
    return {
        "CPEH_NOMBRE_COMISION": settings.CPEH_NOMBRE_COMISION,
        "CPEH_EVENTO_SISMO_FECHA": settings.CPEH_EVENTO_SISMO_FECHA,
    }
