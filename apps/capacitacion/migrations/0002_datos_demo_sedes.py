"""Carga sedes demo — se ejecuta con migrate (Render/producción)."""
from datetime import date, time, timedelta

from django.db import migrations

SEDES_DEMO = [
    ("Universidad Central de Venezuela (UCV)", "ucv", "Los Chaguaramos", "Caracas", "Distrito Capital"),
    ("Universidad Católica Andrés Bello (UCAB)", "ucab", "Montalbán", "Caracas", "Distrito Capital"),
    ("Universidad de Carabobo (UC)", "uc", "Ciudad Universitaria", "Valencia", "Carabobo"),
    ("Auditorio CIV — Caracas", "civ-caracas", "La Candelaria", "Caracas", "Distrito Capital"),
]


def cargar_datos_demo(apps, schema_editor):
    Campana = apps.get_model("capacitacion", "Campana")
    Sede = apps.get_model("capacitacion", "Sede")
    Sesion = apps.get_model("capacitacion", "Sesion")

    campana, _ = Campana.objects.get_or_create(
        nombre="Capacitación inspectores post-sismo 2026",
        defaults={
            "descripcion": "Inducciones masivas — Comisión Presidencial Habitabilidad",
            "activa": True,
            "fecha_inicio": date(2026, 7, 1),
            "fecha_fin": date(2026, 7, 31),
            "responsable_nombre": "Ing. Francisco Garcés",
        },
    )

    for nombre, slug, direccion, municipio, estado in SEDES_DEMO:
        sede, _ = Sede.objects.update_or_create(
            slug=slug,
            defaults={
                "campana_id": campana.pk,
                "nombre": nombre,
                "direccion": direccion,
                "municipio": municipio,
                "estado": estado,
                "activa": True,
                "responsable_nombre": campana.responsable_nombre,
            },
        )
        dia = date.today()
        dias = 0
        while dias < 10:
            if dia.weekday() < 5:
                for hora in (time(9, 0), time(14, 0)):
                    Sesion.objects.get_or_create(
                        sede_id=sede.pk,
                        fecha=dia,
                        hora=hora,
                        defaults={"cupo": 100, "estado": "programada"},
                    )
                dias += 1
            dia += timedelta(days=1)


def revertir(apps, schema_editor):
    Sede = apps.get_model("capacitacion", "Sede")
    Campana = apps.get_model("capacitacion", "Campana")
    Sede.objects.filter(slug__in=[s[1] for s in SEDES_DEMO]).delete()
    Campana.objects.filter(nombre="Capacitación inspectores post-sismo 2026").delete()


class Migration(migrations.Migration):
    dependencies = [
        ("capacitacion", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(cargar_datos_demo, revertir),
    ]
