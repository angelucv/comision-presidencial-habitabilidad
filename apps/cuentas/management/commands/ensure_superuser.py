"""Crea o actualiza el superusuario inicial (idempotente, para deploy)."""
import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Crea o actualiza el superusuario definido en variables de entorno."

    def handle(self, *args, **options):
        username = os.environ.get("DJANGO_SUPERUSER_USERNAME", "").strip()
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD", "").strip()
        email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "").strip()

        if not username or not password:
            self.stdout.write(
                self.style.WARNING(
                    "Superusuario omitido: configure DJANGO_SUPERUSER_USERNAME y "
                    "DJANGO_SUPERUSER_PASSWORD."
                )
            )
            return

        if not email:
            email = f"{username}@cpeh.local"

        User = get_user_model()
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                "email": email,
                "is_staff": True,
                "is_superuser": True,
            },
        )

        user.email = email
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save()

        if created:
            self.stdout.write(self.style.SUCCESS(f"Superusuario creado: {username}"))
        else:
            self.stdout.write(self.style.SUCCESS(f"Superusuario actualizado: {username}"))
