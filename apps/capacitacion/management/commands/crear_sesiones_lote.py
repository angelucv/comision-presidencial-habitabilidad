"""Crea sesiones en lote para una sede (días de semana + rango de fechas)."""
from datetime import date, time, timedelta

from django.core.management.base import BaseCommand, CommandError

from apps.capacitacion.models import Sesion


class Command(BaseCommand):
    help = "Genera sesiones en lote: sede, desde, hasta, días LMXJV, hora, cupo."

    def add_arguments(self, parser):
        parser.add_argument("--sede-id", type=int, required=True)
        parser.add_argument("--desde", type=str, required=True, help="YYYY-MM-DD")
        parser.add_argument("--hasta", type=str, required=True, help="YYYY-MM-DD")
        parser.add_argument(
            "--dias",
            type=str,
            default="0,1,2,3,4",
            help="Días de semana 0=lun … 6=dom, separados por coma",
        )
        parser.add_argument("--hora", type=str, default="09:00", help="HH:MM")
        parser.add_argument("--cupo", type=int, default=80)
        parser.add_argument("--dry-run", action="store_true")

    def handle(self, *args, **options):
        from apps.capacitacion.models import Sede

        try:
            sede = Sede.objects.get(pk=options["sede_id"])
        except Sede.DoesNotExist as exc:
            raise CommandError(f"Sede id={options['sede_id']} no existe") from exc

        desde = date.fromisoformat(options["desde"])
        hasta = date.fromisoformat(options["hasta"])
        hora = time.fromisoformat(options["hora"])
        dias = {int(d.strip()) for d in options["dias"].split(",") if d.strip() != ""}

        creadas = 0
        omitidas = 0
        dia = desde
        while dia <= hasta:
            if dia.weekday() in dias:
                exists = Sesion.objects.filter(sede=sede, fecha=dia, hora=hora).exists()
                if exists:
                    omitidas += 1
                elif options["dry_run"]:
                    self.stdout.write(f"[dry-run] {sede.nombre} {dia} {hora}")
                    creadas += 1
                else:
                    Sesion.objects.create(
                        sede=sede,
                        fecha=dia,
                        hora=hora,
                        cupo=options["cupo"],
                    )
                    creadas += 1
            dia += timedelta(days=1)

        self.stdout.write(
            self.style.SUCCESS(
                f"Listo: {creadas} sesiones {'simuladas' if options['dry_run'] else 'creadas'}, "
                f"{omitidas} omitidas (duplicadas)."
            )
        )
