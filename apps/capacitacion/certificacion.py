"""Certificación de inspectores y creación de usuarios."""
from __future__ import annotations

import logging
import re
import secrets

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone

from apps.capacitacion.models import Inscripcion

logger = logging.getLogger(__name__)


def _username_desde_cedula(cedula: str) -> str:
    base = re.sub(r"[^a-z0-9]", "", cedula.lower())
    return base[:150] or "inspector"


def _generar_clave_temporal() -> str:
    return secrets.token_urlsafe(10)


def crear_o_actualizar_usuario_inspector(participante) -> tuple[object, str]:
    """Crea usuario Django vinculado al participante. Devuelve (user, clave_temporal)."""
    User = get_user_model()
    username = _username_desde_cedula(participante.cedula)
    clave = _generar_clave_temporal()

    user = participante.usuario
    if user is None:
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                "email": participante.correo or "",
                "first_name": participante.nombres[:150],
                "last_name": participante.apellidos[:150],
                "is_staff": False,
                "is_active": True,
            },
        )
        if not created:
            suffix = 1
            while User.objects.filter(username=f"{username}{suffix}").exists():
                suffix += 1
            user = User.objects.create_user(
                username=f"{username}{suffix}",
                email=participante.correo or "",
                first_name=participante.nombres[:150],
                last_name=participante.apellidos[:150],
            )
        participante.usuario = user
        participante.save(update_fields=["usuario"])
    else:
        if participante.correo and user.email != participante.correo:
            user.email = participante.correo
            user.save(update_fields=["email"])

    user.set_password(clave)
    user.is_active = True
    user.save(update_fields=["password", "is_active"])

    grupo, _ = Group.objects.get_or_create(name="Inspector")
    user.groups.add(grupo)

    return user, clave


def enviar_correo_certificado(inscripcion: Inscripcion, user, clave_temporal: str, request=None) -> bool:
    participante = inscripcion.participante
    if not participante.correo:
        return False

    from django.conf import settings

    from apps.capacitacion.services import site_base_url

    login_url = f"{site_base_url(request)}/cuentas/login/"
    inspecciones_url = f"{site_base_url(request)}/inspecciones/"

    context = {
        "inscripcion": inscripcion,
        "participante": participante,
        "sesion": inscripcion.sesion,
        "sede": inscripcion.sesion.sede,
        "comision": settings.CPEH_NOMBRE_COMISION,
        "contenido_charla": inscripcion.sesion.contenido_induccion_efectivo(),
        "encargado_charla": inscripcion.encargado_charla or inscripcion.sesion.responsable_efectivo(),
        "username": user.username,
        "clave_temporal": clave_temporal,
        "login_url": login_url,
        "inspecciones_url": inspecciones_url,
    }
    subject = f"Certificado de inducción ERD — {inscripcion.codigo}"
    body = render_to_string("capacitacion/email/certificado_induccion.txt", context)
    html_body = render_to_string("capacitacion/email/certificado_induccion.html", context)

    try:
        send_mail(
            subject=subject,
            message=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[participante.correo],
            html_message=html_body,
            fail_silently=False,
        )
        return True
    except Exception:
        logger.exception(
            "No se pudo enviar certificado a %s (inscripción %s)",
            participante.correo,
            inscripcion.codigo,
        )
        return False


def certificar_inscripcion(
    inscripcion: Inscripcion,
    coordinador,
    *,
    encargado_charla: str = "",
    request=None,
) -> tuple[object, str, bool]:
    """
    Marca asistencia y certificación, crea usuario inspector y envía correo.
    Devuelve (user, clave_temporal, correo_enviado).
    """
    inscripcion.asistio = True
    inscripcion.certificado_emitido = True
    inscripcion.certificado_en = timezone.now()
    inscripcion.certificado_por = coordinador
    inscripcion.encargado_charla = (
        encargado_charla.strip() or inscripcion.sesion.responsable_efectivo()
    )
    inscripcion.save(
        update_fields=[
            "asistio",
            "certificado_emitido",
            "certificado_en",
            "certificado_por",
            "encargado_charla",
        ]
    )

    user, clave = crear_o_actualizar_usuario_inspector(inscripcion.participante)
    correo_ok = enviar_correo_certificado(inscripcion, user, clave, request)
    return user, clave, correo_ok
