from django.shortcuts import render

from . import comision_data


def home(request):
    return render(request, "core/home.html")


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
