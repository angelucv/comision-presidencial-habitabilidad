"""Utilidades para inspectores certificados."""
from apps.capacitacion.models import Inscripcion


def usuario_es_inspector_certificado(user) -> bool:
    if not user.is_authenticated:
        return False
    if user.is_staff:
        return True
    return Inscripcion.objects.filter(
        participante__usuario=user,
        certificado_emitido=True,
    ).exists()


def participante_certificado(user):
    if not user.is_authenticated:
        return None
    inscripcion = (
        Inscripcion.objects.filter(
            participante__usuario=user,
            certificado_emitido=True,
        )
        .select_related("participante", "sesion__sede")
        .order_by("-certificado_en")
        .first()
    )
    return inscripcion.participante if inscripcion else None
