"""Envía un correo de prueba para verificar la configuración."""
from django.conf import settings
from django.core.mail import send_mail
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Envía un correo de prueba (SMTP o Brevo según configuración)."

    def add_arguments(self, parser):
        parser.add_argument(
            "destino",
            nargs="?",
            default="",
            help="Correo destino (opcional; usa EMAIL_HOST_USER si no se indica).",
        )

    def handle(self, *args, **options):
        destino = (options["destino"] or settings.EMAIL_HOST_USER or "").strip()
        if not destino:
            raise CommandError("Indique un correo destino o configure EMAIL_HOST_USER.")

        backend = settings.EMAIL_BACKEND
        self.stdout.write(f"Backend: {backend}")
        self.stdout.write(f"From: {settings.DEFAULT_FROM_EMAIL}")
        self.stdout.write(f"To: {destino}")

        try:
            send_mail(
                subject="Prueba CPEH — correo operativo",
                message="Si recibe este mensaje, el envío de correos está configurado correctamente.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[destino],
                fail_silently=False,
            )
        except Exception as exc:
            raise CommandError(f"Falló el envío: {exc}") from exc

        self.stdout.write(self.style.SUCCESS("Correo de prueba enviado correctamente."))
