"""Carga edificaciones de demostración con coordenadas en Venezuela."""
from decimal import Decimal

from django.core.management.base import BaseCommand

from apps.inspecciones.models import Edificacion

EDIFICIOS_DEMO = [
    (
        "Torre Residencial Plaza Venezuela",
        "Av. Universidad, Plaza Venezuela",
        "Libertador",
        "Distrito Capital",
        Decimal("10.493500"),
        Decimal("-66.878000"),
    ),
    (
        "Edificio Los Palos Grandes — Chacao",
        "Calle El Bosque, Los Palos Grandes",
        "Chacao",
        "Miranda",
        Decimal("10.496200"),
        Decimal("-66.848500"),
    ),
    (
        "Conjunto Residencial La Trinidad",
        "Av. Principal La Trinidad",
        "Baruta",
        "Miranda",
        Decimal("10.432100"),
        Decimal("-66.856300"),
    ),
    (
        "Bloque habitacional San Bernardino",
        "Av. Lecuna, San Bernardino",
        "Libertador",
        "Distrito Capital",
        Decimal("10.505800"),
        Decimal("-66.916200"),
    ),
    (
        "Edificio multifamiliar La Candelaria",
        "Av. México, La Candelaria",
        "Libertador",
        "Distrito Capital",
        Decimal("10.508900"),
        Decimal("-66.903400"),
    ),
    (
        "Residencias Universidad de Carabobo",
        "Ciudad Universitaria",
        "Valencia",
        "Carabobo",
        Decimal("10.173600"),
        Decimal("-67.960800"),
    ),
    (
        "Torre en zona sísmica San Felipe",
        "Centro, San Felipe",
        "San Felipe",
        "Yaracuy",
        Decimal("10.335900"),
        Decimal("-68.742500"),
    ),
    (
        "Edificio en Maracay centro",
        "Av. Bolívar",
        "Girardot",
        "Aragua",
        Decimal("10.246900"),
        Decimal("-67.595800"),
    ),
]


class Command(BaseCommand):
    help = "Crea edificaciones demo con coordenadas para el mapa (idempotente por nombre)."

    def handle(self, *args, **options):
        creados = 0
        for nombre, direccion, municipio, estado, lat, lon in EDIFICIOS_DEMO:
            _, created = Edificacion.objects.get_or_create(
                nombre=nombre,
                defaults={
                    "direccion": direccion,
                    "municipio": municipio,
                    "estado": estado,
                    "latitud": lat,
                    "longitud": lon,
                },
            )
            if created:
                creados += 1
        self.stdout.write(
            self.style.SUCCESS(
                f"Edificaciones demo: {creados} nuevas, {len(EDIFICIOS_DEMO) - creados} ya existían."
            )
        )
