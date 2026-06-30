from django.shortcuts import render

from . import comision_data, sistema_data


def home(request):
    return render(
        request,
        "core/home.html",
        {"instituciones_enlaces": comision_data.INSTITUCIONES_ENLACES},
    )


def comision(request):
    return render(
        request,
        "core/comision.html",
        {
            "objetivos": comision_data.OBJETIVOS,
            "miembros": comision_data.MIEMBROS,
            "semaforo": comision_data.SEMAFORO,
            "evento_sismo": comision_data.EVENTO_SISMO,
        },
    )


def como_funciona(request):
    return render(
        request,
        "core/como_funciona.html",
        {
            "roles": sistema_data.ROLES,
            "pasos": sistema_data.PASOS_FLUJO,
            "semaforo": sistema_data.SEMAFORO_RESUMEN,
        },
    )
