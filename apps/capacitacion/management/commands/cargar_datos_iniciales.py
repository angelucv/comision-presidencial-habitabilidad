"""Carga datos iniciales de demostración (campaña, sedes y sesiones)."""
from datetime import date, time, timedelta

from django.core.management.base import BaseCommand

from apps.capacitacion.models import Campana, Sede, Sesion


SEDES_DEMO = [
    ("Universidad Central de Venezuela (UCV)", "ucv", "Los Chaguaramos", "Caracas", "Distrito Capital"),
    ("Universidad Católica Andrés Bello (UCAB)", "ucab", "Montalbán", "Caracas", "Distrito Capital"),
    ("Universidad de Carabobo (UC)", "uc", "Ciudad Universitaria", "Valencia", "Carabobo"),
    ("Auditorio CIV — Caracas", "civ-caracas", "La Candelaria", "Caracas", "Distrito Capital"),
]

HORARIOS = (time(9, 0), time(14, 0))

class Command(BaseCommand):
    help = "Crea campaña, sedes de ejemplo y sesiones (idempotente)."

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
        if not campana.activa:
            campana.activa = True
            campana.save(update_fields=["activa"])

        sedes_creadas = sesiones_creadas = 0

        for nombre, slug, direccion, municipio, estado in SEDES_DEMO:
            sede, created = Sede.objects.update_or_create(
                slug=slug,
                defaults={
                    "campana": campana,
                    "nombre": nombre,
                    "direccion": direccion,
                    "municipio": municipio,
                    "estado": estado,
                    "activa": True,
                    "responsable_nombre": campana.responsable_nombre,
                },
            )
            if created:
                sedes_creadas += 1
                self.stdout.write(f"Sede creada: {nombre}")

            sesiones_creadas += self._crear_sesiones_calendario(sede)

        total_sedes = Sede.objects.filter(activa=True).count()
        total_sesiones = Sesion.objects.filter(estado=Sesion.Estado.PROGRAMADA).count()
        self.stdout.write(
            self.style.SUCCESS(
                f"Listo: {sedes_creadas} sedes nuevas, {sesiones_creadas} sesiones nuevas. "
                f"Total activas: {total_sedes} sedes, {total_sesiones} sesiones programadas."
            )
        )

    def _crear_sesiones_calendario(self, sede: Sede) -> int:
        """Sesiones pasadas (retroactivo) y futuras en días hábiles."""
        creadas = 0
        dia = date.today() - timedelta(days=14)
        fin = date.today() + timedelta(days=21)
        while dia <= fin:
            if dia.weekday() < 5:
                for hora in HORARIOS:
                    _, created = Sesion.objects.get_or_create(
                        sede=sede,
                        fecha=dia,
                        hora=hora,
                        defaults={"cupo": 100, "estado": Sesion.Estado.PROGRAMADA},
                    )
                    if created:
                        creadas += 1
            dia += timedelta(days=1)
        return creadas
