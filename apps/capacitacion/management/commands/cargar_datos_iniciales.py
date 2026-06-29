"""Carga datos iniciales de demostración (campaña, sedes de ejemplo)."""
from datetime import date, time, timedelta

from django.core.management.base import BaseCommand

from apps.capacitacion.models import Campana, Sede, Sesion


class Command(BaseCommand):
    help = "Crea campaña y sedes de ejemplo para pruebas locales."

    def handle(self, *args, **options):
        campana, _ = Campana.objects.get_or_create(
            nombre="Capacitación inspectores post-sismo 2026",
            defaults={
                "descripcion": "Inducciones masivas en universidades — Comisión Presidencial Habitabilidad",
                "activa": True,
                "fecha_inicio": date(2026, 7, 1),
                "fecha_fin": date(2026, 7, 31),
                "responsable_nombre": "Ing. Francisco Garcés",
            },
        )

        sedes_data = [
            ("Universidad Central de Venezuela (UCV)", "ucv", "Los Chaguaramos", "Caracas", "Distrito Capital"),
            ("Universidad Católica Andrés Bello (UCAB)", "ucab", "Montalbán", "Caracas", "Distrito Capital"),
            ("Universidad de Carabobo (UC)", "uc", "Ciudad Universitaria", "Valencia", "Carabobo"),
            ("Auditorio CIV — Caracas", "civ-caracas", "La Candelaria", "Caracas", "Distrito Capital"),
        ]

        for nombre, slug, direccion, municipio, estado in sedes_data:
            sede, created = Sede.objects.get_or_create(
                slug=slug,
                defaults={
                    "campana": campana,
                    "nombre": nombre,
                    "direccion": direccion,
                    "municipio": municipio,
                    "estado": estado,
                    "activa": True,
                },
            )
            if created:
                self.stdout.write(f"Sede creada: {nombre}")
                # Próximos 5 días hábiles a las 09:00
                dia = date.today() + timedelta(days=1)
                count = 0
                while count < 5:
                    if dia.weekday() < 5:
                        Sesion.objects.get_or_create(
                            sede=sede,
                            fecha=dia,
                            hora=time(9, 0),
                            defaults={"cupo": 100},
                        )
                        count += 1
                    dia += timedelta(days=1)

        self.stdout.write(self.style.SUCCESS("Datos iniciales listos."))
